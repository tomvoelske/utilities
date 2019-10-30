import csv
import os


def analyser():
    root_dir = r'E:\scripts\AMEX Analyser'
    csv_list = [root_dir + os.sep + x for x in os.listdir(root_dir) if '.csv' in x]

    date_dict = {}
    cost_dict = {}
    analytic_dict = {'average': 0.00}
    reference_list = []

    for csv_path in csv_list:
        with open(csv_path, 'r') as csv_file:
            csv_data = csv.reader(csv_file)
            for csv_line in csv_data:
                reference = csv_line[1]
                if reference in reference_list:
                    # prevents processing of duplicates
                    continue
                raw_cost = csv_line[2].strip()
                if '-' in raw_cost:
                    # don't care about money paid back
                    continue
                cost = round(float(raw_cost), 2)
                reference_list.append(reference)
                date = get_date(csv_line[0])
                if date not in date_dict.keys():
                    date_dict[date] = {}
                    analytic_dict[date] = {'total': 0.00}
                output = csv_line[3].strip()
                if 'AMAZON' in output:
                    output = 'AMAZON'
                if output not in date_dict[date].keys():
                    date_dict[date][output] = 0.00
                date_dict[date][output] += cost
                analytic_dict[date]['total'] += cost
                analytic_dict['average'] += cost
                if output not in cost_dict.keys():
                    cost_dict[output] = 0.00
                cost_dict[output] += cost
                cost_dict[output] = round(cost_dict[output], 2)

    analytic_dict['average'] /= (len(analytic_dict.keys()) - 1)
    average_monthly_spending = analytic_dict['average']

    print('EXPENDITURES BY MONTH\n')

    # handling each month
    for date in date_dict.keys():
        print(date + '\n')
        descending_spendings = descending_sort_spends(date_dict[date])
        total_spending = analytic_dict[date]['total']
        for merchant in descending_spendings:
            spending = date_dict[date][merchant]
            average = round((spending / total_spending) * 100, 2)
            print('{0}: £{1:.2f} ({2:.2f}%)'.format(merchant, spending, average))

        monthly_average = round((total_spending / average_monthly_spending) * 100, 2)

        print('MONTHLY TOTAL: £{0:.2f} ({1:.2f}% OF AVERAGE MONTHLY SPENDINGS)'.format(total_spending, monthly_average))
        print('')

    print('EXPENDITURES BY SOURCE\n')

    # handling each source

    n_months = len(date_dict.keys())

    for source in cost_dict.keys():
        print(source + '\n')
        for date in date_dict.keys():
            try:
                print('{0}: £{1:.2f}'.format(date, date_dict[date][source]))
            except KeyError:
                print('{0}: £0.00'.format(date))
        average_monthly_source = round((cost_dict[source] / n_months), 2)
        print('TOTAL: £{0:.2f}'.format(cost_dict[source]))
        print('AVERAGE: £{0:.2f}'.format(average_monthly_source))
        print('')


def get_date(date):
    month = date.split('/')[1]
    year = date.split('/')[2]
    return month + ' ' + year


def descending_sort_spends(spendings):
    return sorted(spendings, key=spendings.get, reverse=True)


if __name__ == '__main__':
    analyser()
