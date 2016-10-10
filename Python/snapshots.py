#!/usr/bin/python
import subprocess
import datetime
import operator
import time
from datetime import tzinfo

class UTC(tzinfo):

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return datetime.timedelta(0)

utc = UTC()

class ZfsSnapshot:
    def __init__(self, path, name, time):
        self._path = path
        self._name = name
        self._time = time

    def get_path(self):
        return self._path

    def get_time(self):
        return self._time

    def get_name_tag(self):
        # Gets the part after the @. The name and the date, without the path.
        return self._time.strftime(self._name + '-%Y.%m.%d-%H.%M.%S')

def get_snapshots(pool_path, snapshot_name):
    
    output = subprocess.check_output(['zfs', 'list', '-Ht', 'snapshot']).decode('utf-8').split('\n')
    
    long_snapshots = [line.split('\t') for line in output]
    snapshot_full_names = [line[0] for line in long_snapshots]

    # List of all snapshots.
    snapshots = []

    for snap in snapshot_full_names:
        path = snap[:snap.find('@')]
        
        # Snapshots are recursive, only need top level path.
        if path != pool_path:
            continue

        name_and_date = snap[snap.find('@') + 1:]

        if name_and_date.startswith(snapshot_name):
              
            name = snapshot_name
            
            utc_time = time.strptime(name_and_date[name_and_date.find('-') + 1:], '%Y.%m.%d-%H.%M.%S')
            snap_time = datetime.datetime(utc_time[0], utc_time[1], utc_time[2], utc_time[3], utc_time[4], utc_time[5], tzinfo = utc)

            snapshots.append(ZfsSnapshot(path, name, snap_time))

    return snapshots

def take_snapshot(pool_path, snapshot_name):
    
    time = datetime.datetime.utcnow()
    full_name = time.strftime(snapshot_name + '-%Y.%m.%d-%H.%M.%S')
    subprocess.check_call(['zfs', 'snapshot', '-r', '{}@{}'.format(pool_path, full_name)])
    subprocess.check_call(['logger', '-t', 'snapshots', 'Took a Snapshot: {}'.format(full_name)])
    return ZfsSnapshot(pool_path, snapshot_name, time)

def delete_snapshot(pool_path, snapshot):
    subprocess.check_call(['zfs', 'destroy', '-r', '{}@{}'.format(snapshot.get_path(), snapshot.get_name_tag())])
    subprocess.check_call(['logger', '-t', 'snapshots', 'Deleted snapshot: {}'.format(snapshot.get_name_tag())])

def get_last_per_time_group(groups):
    last_per = []

    for group in groups.values():
        last_per.append(sorted(group, key=operator.methodcaller('get_time'))[-1])

    return last_per

def get_last_per_hour(snapshots):
    # Make groups for each hour.
    hours = {}

    for snapshot in snapshots:
        time = snapshot.get_time()
        hour = datetime.datetime(year = time.year, month = time.month, day = time.day, hour=time.hour, tzinfo = time.tzinfo)

        if hour not in hours:
            hours[hour] = []
        hours[hour].append(snapshot)

    return get_last_per_time_group(hours)

def get_last_per_day(snapshots):
    
    days = {}

    for snapshot in snapshots:
        time = snapshot.get_time()
        day = datetime.datetime(year = time.year, month = time.month, day = time.day, tzinfo = time.tzinfo)

        if day not in days:
            days[day] = []
        days[day].append(snapshot)

    return get_last_per_time_group(days)

def get_last_per_month(snapshots):

    months = {}

    for snapshot in snapshots:
        time = snapshot.get_time()
        month = datetime.datetime(year = time.year, month = time.month, day = 1, tzinfo = time.tzinfo)

        if month not in months:
            months[month] = []
        months.append(snapshot)

    return get_last_per_time_group(months)

def group_by_age(snapshots):
    
    age_groups = ([], [], [], [])

    cur_time = datetime.datetime.now(utc)

    for snapshot in snapshots:
        age = cur_time - snapshot.get_time()

        if age >= datetime.timedelta(days = 365):
            age_groups[0].append(snapshot)
            continue

        if age > datetime.timedelta(days = 30):
            age_groups[1].append(snapshot)
            continue

        if age > datetime.timedelta(days = 2):
            age_groups[2].append(snapshot)
            continue

        age_groups[3].append(snapshot)

    return age_groups

def mark_for_deletion(snapshots):
    
    to_keep = set()

    age_groups = group_by_age(snapshots)

    to_keep.update(age_groups[0])

    to_keep.update(get_last_per_month(age_groups[1]))

    to_keep.update(get_last_per_day(age_groups[2]))

    to_keep.update(get_last_per_hour(age_groups[3]))


    to_delete = set(snapshots)
    to_delete.difference_update(to_keep)

    return sorted(to_delete, key = operator.methodcaller('get_time'), reverse = True)


if __name__=='__main__':

    take_snapshot('tank/ROOT', 'Snaps')
    snapshots = get_snapshots('tank/ROOT', 'Snaps')
    to_delete = mark_for_deletion(snapshots)
    for snapshot in to_delete:
        print(snapshot.get_name_tag())
        delete_snapshot('tank/ROOT', snapshot)
