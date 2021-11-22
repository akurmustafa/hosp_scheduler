# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import random
import io_util
from datetime import datetime, date, timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

def get_weekdays_between(start_date, end_date):
    weekday_count = 0
    weekend_count = 0
    for cur_date in daterange(start_date, end_date):
        weekday = cur_date.weekday()
        if weekday < 5:
            weekday_count += 1
        elif weekday < 7:
            weekend_count += 1
        else:
            assert 0
        # print(weekday, cur_date)
    return weekday_count, weekend_count


def distribute_labour(labour, n_person):
    avg_labour = labour//n_person
    missing_labor = labour-avg_labour*n_person
    person_labours = list()
    for i in range(n_person):
        person_labours.append(avg_labour)
    for k in range(missing_labor):
        person_labours[k] += 1
    random.shuffle(person_labours)
    return person_labours


def get_all_distributions(job_dict, mode):
    dists = list()
    for cur_job in job_dict.keys():
        if mode in job_dict[cur_job].keys():
            dists.append(job_dict[cur_job][mode]['dist'])
    return dists


def get_totals(dist):
    totals = [0 for i in range(len(dist[0]))]
    for cur_task in dist:
        for idx, cur_labour in enumerate(cur_task):
            totals[idx] += cur_labour      
    return totals


def correct_distributions(dist):
    totals = get_totals(dist)
    sorted_indices = [i[0] for i in sorted(enumerate(totals), key=lambda x: x[1])]
    while max(totals)-min(totals)>1:
        for cur_task in dist:
            if cur_task[sorted_indices[-1]]-cur_task[sorted_indices[0]]>0:
                cur_task[sorted_indices[-1]], cur_task[sorted_indices[0]] = cur_task[sorted_indices[0]], cur_task[sorted_indices[-1]]
                totals = get_totals(dist)
                sorted_indices = [i[0] for i in sorted(enumerate(totals), key=lambda x: x[1])]
                print(totals)
    return dist, totals

def main():
    dataset = io_util.read_from_json('./persons.json')
    start_date_str = dataset['date_start']
    end_date_str = dataset['date_end']
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    weekday_count, weekend_count = get_weekdays_between(start_date, end_date)
    job_labour = dict()
    mode_list = [('weekday', weekday_count), ('weekend', weekend_count)]

    for cur_mode, cur_mode_count in mode_list:
        for job_name in dataset[cur_mode]['jobs'].keys():
            if job_name not in job_labour.keys():
                job_labour[job_name] = dict()
            cur_mode_labour = cur_mode+'_labour'
            if cur_mode not in job_labour[job_name].keys():
                job_labour[job_name][cur_mode] = dict()
            if 'total_labour' not in job_labour[job_name][cur_mode].keys():
                job_labour[job_name][cur_mode]['total_labour'] = 0
            job_labour[job_name][cur_mode]['total_labour'] += dataset[cur_mode]['jobs'][job_name]['required_personnel']*cur_mode_count
    print(job_labour)

    n_person = len(dataset['persons'])
    for cur_job in job_labour.keys():
        for cur_mode in job_labour[cur_job].keys():
            job_labour[cur_job][cur_mode]['dist'] = distribute_labour(job_labour[cur_job][cur_mode]['total_labour'], n_person)
    print(job_labour)
    weekend_distributions =get_all_distributions(job_labour, 'weekend')
    weekend_new_dist, weekend_totals = correct_distributions(weekend_distributions)
    weekday_distributions = get_all_distributions(job_labour, 'weekday')
    weekday_new_dist, weekday_totals = correct_distributions(weekday_distributions)

    pass
    # persons = dict()
    # for cur_person in dataset['persons'].keys():
    #     persons[cur_person] = dict()
    #     persons[cur_person]
    #
    # schedule = dict()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
