import logging

class plausability_tests:
    '''
    e_flows_df can include columns with titles...
    'Demand'
    'Demand shortage'
    'Demand supplied'
    'PV generation'
    'Excess electricity'
    'Consumption from main grid (MG side)'
    'Feed into main grid (MG side)'
    'Consumption from main grid (utility side)'
    'Feed into main grid (utility side)'
    'Storage discharge'
    'Storage charge'
    'Genset generation'
    'Excess generation'
    'PV generation'
    'Grid availability'
    '''
    def run(oemof_results, e_flows_df):
        '''
        Checking oemof calculations for plausability. The most obvious errors should be identified this way.
        Ideally, not a single error should be displayed or added to the oemof comments.
        Checks include:
        - storage charge <-> dicharge
        - Demand <-> supplied demand <-> shortage
        - feedin <-> consumption
        - grid availability <-> feedin to grid
        - grid availability <-> consumption from grid
        - excess <-> shortage
        - excess <-> feedin > pcc cap and excess <-> grid availability
        '''
        plausability_tests.charge_discharge(oemof_results, e_flows_df)
        plausability_tests.demand_supply_shortage(oemof_results, e_flows_df)
        plausability_tests.feedin_consumption(oemof_results, e_flows_df)
        plausability_tests.gridavailability_consumption(oemof_results, e_flows_df)
        plausability_tests.gridavailability_feedin(oemof_results, e_flows_df)
        plausability_tests.excess_shortage(oemof_results, e_flows_df)
        plausability_tests.excess_feedin(oemof_results, e_flows_df)
        return


    def charge_discharge (oemof_results, e_flows_df):
        logging.debug('Plausibility test: Charge/Discharge')
        if ('Storage discharge' in e_flows_df.columns and 'Storage charge' in e_flows_df.columns):
            boolean = True

            test = [(e_flows_df['Storage discharge'][t] != 0 and e_flows_df['Storage charge'][t] == 0) for t in e_flows_df.index]

            if any(test) == False:
                boolean = False

            if boolean == False:
                logging.warning("PLAUSABILITY TEST FAILED: Charge and discharge of batteries at the same time!")
                oemof_results.update({'comments': oemof_results['comments'] + 'Charge and discharge of batteries at the same time. '})
        return

    def demand_supply_shortage (oemof_results, e_flows_df):
        logging.debug('Plausibility test: Demand/Supply/Shortage')
        if (('Demand supplied' in e_flows_df.columns)
                and ('Demand' in e_flows_df.columns)
                and ('Demand shortage' in e_flows_df.columns)):

            boolean = True

            test = [((e_flows_df['Demand supplied'][t] == e_flows_df['Demand'][t] and e_flows_df['Demand shortage'][t] == 0)
                    or ((e_flows_df['Demand supplied'][t] != e_flows_df['Demand'][t] and e_flows_df['Demand shortage'][t] != 0)))
                    for t in e_flows_df.index]

            if any(test) == False:
                boolean = False

            if boolean == False:
                logging.warning("PLAUSABILITY TEST FAILED: Demand not fully supplied but no shortage!")
                oemof_results.update({'comments': oemof_results['comments'] + 'Demand not fully supplied but no shortage. '})

        return


    def feedin_consumption(oemof_results, e_flows_df):
        logging.debug('Plausibility test: Feedin/Consumption')
        if (('Consumption from main grid' in e_flows_df.columns)
                and ('Feed into main grid' in e_flows_df.columns)):

            boolean = True

            test = [(e_flows_df['Consumption from main grid'][t] != 0 and e_flows_df['Feed into main grid'][t] != 0)
                    for t in e_flows_df.index]

            if any(test) == False:
                boolean = False

            if boolean == False:
                logging.warning("PLAUSABILITY TEST FAILED: Feedin to and consumption from national grid at the same time!")
                oemof_results.update(
                    {'comments': oemof_results['comments'] + 'Feedin to and consumption from national grid at the same time. '})

        return

    def gridavailability_feedin(oemof_results, e_flows_df):
        logging.debug('Plausibility test: Grid availability/Feedin')
        if (('Consumption from main grid' in e_flows_df.columns)
                and ('Feed into main grid' in e_flows_df.columns)):

            boolean = True

            test = [(e_flows_df['Feed into main grid'][t] != 0 and e_flows_df['Grid availability'][t] == 0)
                    for t in e_flows_df.index]

            if any(test) == False:
                boolean = False

            if boolean == False:
                logging.warning("PLAUSABILITY TEST FAILED: Feedin to national grid during blackout!")
                oemof_results.update(
                    {'comments': oemof_results['comments'] + 'Feedin to national grid during blackout. '})

        return

    def gridavailability_consumption(oemof_results, e_flows_df):
        logging.debug('Plausibility test: Grid availability consumption')
        if (('Consumption from main grid' in e_flows_df.columns)
                and ('Grid availability' in e_flows_df.columns)):

            boolean = True

            test = [(e_flows_df['Consumption from main grid'][t] != 0 and e_flows_df['Grid availability'][t] == 0)
                    for t in e_flows_df.index]

            if any(test) == False:
                boolean = False

            if boolean == False:
                logging.warning("PLAUSABILITY TEST FAILED: Consumption from national grid during blackout!")
                oemof_results.update(
                    {'comments': oemof_results['comments'] + 'Consumption from national grid during blackout. '})

        return

    def excess_shortage(oemof_results, e_flows_df):
        logging.debug('Plausibility test: Excess/shortage')
        if (('Excess electricity' in e_flows_df.columns)
                and ('Demand shortage' in e_flows_df.columns)):

            boolean = True

            test = [(e_flows_df['Excess electricity'][t] != 0 and e_flows_df['Demand shortage'][t] != 0)
                    for t in e_flows_df.index]

            if any(test) == False:
                boolean = False

            if boolean == False:
                logging.warning("PLAUSABILITY TEST FAILED: Excess and shortage at the same time!")
                oemof_results.update(
                    {'comments': oemof_results['comments'] + 'Excess and shortage at the same time. '})

        return


    def excess_feedin(oemof_results, e_flows_df):
        logging.debug('Plausibility test: Excess/Feedin')
        if (('Excess electricity' in e_flows_df.columns)
                and ('Grid availability' in e_flows_df.columns)
                and ('Feed into main grid' in e_flows_df.columns)):

            boolean = True

            test = [(((e_flows_df['Excess electricity'][t] != 0)
                      and (e_flows_df['Feed into main grid'][t] != oemof_results['capacity pcc'][t])) # actual item!
                    or
                    ((e_flows_df['Excess electricity'][t] != 0) and (e_flows_df['Grid availability'][t] == 0)))
                    for t in e_flows_df.index]

            if any(test) == False:
                boolean = False

            if boolean == False:
                logging.warning("PLAUSABILITY TEST FAILED: Excess while feedin to national grid not maximal (PCC capacity)!")
                oemof_results.update(
                    {'comments': oemof_results['comments'] + 'Excess while feedin not maximal.'})

        return