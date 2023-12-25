def get_category_freq(no_etfs):
    #[equity, commodity, bonds, real estate]
    freq_dict = {5:[2, 1, 1, 1],
                10:[3, 2, 3, 2],
                15:[5, 3, 4, 3]
                }
    return freq_dict[no_etfs]