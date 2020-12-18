#!/usr/bin/env python3

# Import utils- and plot-specific modules
from modules_plot import *
from utils.modules_utils import *

import matplotlib.gridspec as gridspec

#====================================================================
def plot_atmosphere( output_dir, sub_dirs ):

    # article class text width is 4.7747 inches
    # http://tex.stackexchange.com/questions/39383/determine-text-width
    # logger.info( 'building stacked interior atmosphere' )

    width   = 12.00 #* 3.0/2.0
    height  = 5.0
    
    # fig_o   = su.FigureData( 1, 3, width, height, output_dir+'/compare_sfd+melt', units='kyr' )
    # fig_o.fig.subplots_adjust(wspace=0.15, hspace=0.0)

    

    # ax0 = fig_o.ax[0]#[0]
    # ax1 = fig_o.ax[1]#[1]
    # ax2 = fig_o.ax[2]#[0]
    # # ax3 = fig_o.ax[1][1]

    # Define figure with gridspec
    # https://matplotlib.org/3.2.1/tutorials/intermediate/gridspec.html
    fig = plt.figure(tight_layout=True, constrained_layout=False, figsize=[width, height])

    gs = fig.add_gridspec(nrows=1, ncols=2, wspace=0.1, hspace=0.25, left=0.055, right=0.98, top=0.98, bottom=0.09)


    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])
    # ax2 = fig.add_subplot(gs[1, 1])

    # ax0b = fig.add_subplot(gs[0, 2:4])
    # ax1b = fig.add_subplot(gs[1, 2])
    # ax2b = fig.add_subplot(gs[1, 3])

    # sns.set_style("ticks")
    # sns.despine()

    
    handle_l = [] # handles for legend

    ymax_atm_pressure   = 0
    ymin_atm_pressure   = 1000
    ymax_atm_z          = 0
    ymin_atm_z          = 0
    ymax_sp_flux        = 0
    xmin                = 0
    xmax                = 0.1

    fs_legend   = 11
    fs_label    = 11

    # Initiate legends
    legend_ax0_handles = []
    legend_ax1_handles = []
    legend_ax1_dummy_handles = []

    # Show wavelenght or wavenumber
    print_wavelength = True

    # Define smoothing length
    nsmooth = 1

    # # Load runtime helpfile
    # runtime_helpfile = pd.read_csv(output_dir+"runtime_helpfile.csv")

    
    data_file_photosphere = '../data/fig8_cff/photosphere.json'
    if os.path.exists(data_file_photosphere):
        a_file = open(data_file_photosphere, "r")
        output = a_file.read()
        print(output)
    else:
        photosphere = {}

    for ni, subdir in enumerate(sub_dirs):

        settings = [ "" ]

        color_idx   = 5

        if ni == 0:
            lw = 1.5
            ls = "-"
        if ni == 1:
            lw = 1.5
            ls = "--"
        if ni == 2:
            lw = 1.5
            ls = ":"
        if ni == 3:
            lw = 1.5
            ls = "-."
        if ni == 4:
            lw = 1.5
            ls = (0, (2, 1))

        ls="-"

        for nn, setting in enumerate( settings ):

            if setting == "":
                setting_name = "(a) Fiducial case"
            if setting == "_mix":
                setting_name = r"(b) Variable $\mathcal{L}$"
            if setting == "_sep":
                setting_name = r"(c) Solid–melt sep."
            if setting == "_utbl":
                setting_name = r"(d) Boundary layer"
            if setting == "_sep_mix":
                setting_name = r"Variable $\mathcal{L}$"+"\n"+"+ solid–melt sep."
            if setting == "_sep_mix_utbl":
                setting_name = r"Variable $\mathcal{L}$"+"\n"+"+ solid–melt sep."+"\n"+"+ UTBL"

            data_dir = output_dir+"/"+subdir+setting

            print(data_dir)

            # Read in time sequences
            data_times = su.get_all_output_times(data_dir)
            keys = ( ('atmosphere','mass_liquid'),
                       ('atmosphere','mass_solid'),
                       ('atmosphere','mass_mantle'),
                       ('atmosphere','mass_core'),
                       ('atmosphere','temperature_surface'),
                       ('atmosphere','emissivity'),
                       ('rheological_front_phi','phi_global'),
                       ('atmosphere','Fatm'),
                       ('atmosphere','pressure_surface'),
                       ('rheological_front_dynamic','depth'),
                       ('rheological_front_dynamic','mesh_index')
                       )
            data = su.get_dict_surface_values_for_times( keys, data_times, data_dir )
            mass_liquid         = data[0,:]
            mass_solid          = data[1,:]
            mass_mantle         = data[2,:]
            mass_core           = data[3,:]
            T_surf              = data[4,:]
            emissivity          = data[5,:]
            phi_global          = data[6,:]
            Fatm                = data[7,:]
            P_surf              = data[8,:]
            rheol_front         = data[9,:]
            rheol_front_idx     = data[10,:]

            # FIND SPECIFIC TIMESTAMP

            # Find critical parameter
            RF_depth_crit = 0.01
            # print(rheol_front/np.max(rheol_front))
            RF_depth_crit_num, RF_depth_crit_idx = find_nearest(rheol_front/np.max(rheol_front), RF_depth_crit)
            RF_depth_crit_time   = data_times[RF_depth_crit_idx]
            
            # RF_half_depth, RF_half_depth_idx = find_nearest(rheol_front, 0.5)
            # RF_half_depth_time   = data_times[RF_half_depth_idx]
            # Phi_global_intersect = phi_global[RF_half_depth_idx]
            # print("RF:", RF_half_depth_idx, RF_half_depth, RF_half_depth_time, Phi_global_intersect)

            phi_crit = 0.2
            phi_crit_num, phi_crit_idx = find_nearest(phi_global, phi_crit)
            phi_crit_time = data_times[phi_crit_idx]
            # print("RF:", phi_crit_idx, RF_half_depth, RF_half_depth_time, Phi_global_intersect)

            Fatm_crit = 1e+3
            Fatm_crit_num, Fatm_crit_idx = find_nearest(Fatm, Fatm_crit)
            Fatm_crit_time = data_times[Fatm_crit_idx]

            # Define output time based on which criterion
            if setting == "":
                
                output_time =  RF_depth_crit_time


            # Find data_time closest to output_time wanted
            atm_data_times = su.get_all_output_pkl_times(data_dir)
            # print(atm_data_times)
            time, time_idx = find_nearest(atm_data_times, output_time)

            # Find planet mass and radius
            myjson_o  = su.MyJSON( data_dir+'/{}.json'.format(data_times[0]) )
            xx_radius = myjson_o.get_dict_values(['data','radius_b'])*1.0E-3
            r_planet  = np.max(xx_radius*1e3) # m
            core_mass   = myjson_o.get_dict_values(['atmosphere','mass_core'])
            mantle_mass = myjson_o.get_dict_values(['atmosphere','mass_mantle'])
            planet_mass = core_mass + mantle_mass

            print(subdir, setting, output_time)


            atm_file = data_dir+"/"+str(int(time))+"_atm.pkl"

            # Read pickle file
            atm_file_stream = open(atm_file,'rb')
            atm = pkl.load(atm_file_stream)
            atm_file_stream.close()

            # color = fig_o.get_color( nn )
            color   = vol_colors[subdir][color_idx]
          
            dirs = {"output": output_dir, "rad_conv": "/Users/tim/bitbucket/pcd_couple-interior-atmosphere/atm_rad_conv"}
            atm = atm_rad_conv.SocRadModel.radCompSoc(atm, dirs, recalc=False, calc_cf=True)

            # Total CFF, normalized
            cff_tot = atm.cff/np.sum(atm.cff)
            prs     = atm.p/np.max(atm.p)

            # Annotate height and pressure of CFF peak
            # For H2 cut out lowermost peak
            cut_idx = len(atm.p)
            if subdir =="H2": cut_idx = -10
            z_profile = AtmosphericHeight(atm, planet_mass, r_planet)*1e-3 # km
            cff_max, cff_max_idx = find_nearest(cff_tot[:cut_idx], np.max(cff_tot[:cut_idx]))
            print("HEIGHT_max, PRS, TMP:", cff_max, cff_max_idx, z_profile[cff_max_idx], "km", atm.p[cff_max_idx]/1e+5, "bar", atm.tmp[cff_max_idx], "K")

            
            # print "max" or "weighted"
            output_label = "weighted"

            # print(np.average(z_profile, weights=cff_tot))

            # Weighted by CFF
            if output_label == "weighted":
                time_print  = latex_float(output_time)
                z_print     = round(np.average(z_profile, weights=cff_tot))
                prs_print   = round(np.average(atm.p/1e+5, weights=cff_tot),1)
                tmp_print   = round(np.average(atm.tmp, weights=cff_tot))
            # At max
            if output_label == "max":
                time_print  = latex_float(output_time)
                z_print     = round(z_profile[cff_max_idx])
                prs_print   = round(atm.p[cff_max_idx]/1e+5,1)
                tmp_print   = round(atm.tmp[cff_max_idx])


            # Label with time
            label_a = vol_latex[subdir]+", "+latex_float(output_time)+" yr"
            # Label w/o time
            label_a = vol_latex[subdir]
            # Label with time, height, pressure and temperature
            label_a = vol_latex[subdir]+": "+str(time_print)+" yr, "+str(z_print)+" km, "+str(prs_print)+" bar, "+str(tmp_print)+" K"
            # Label with time, height, pressure
            label_a = vol_latex[subdir]+": "+str(z_print)+" km, "+str(prs_print)+" bar"

            # Plot a line at the max location
            print(cff_tot[cff_max_idx], prs[cff_max_idx], prs[cff_max_idx])
            if output_label == "max":
                ax0.plot([cff_tot[cff_max_idx], cff_tot[cff_max_idx]], [3e-5, prs[cff_max_idx]], ls="--", lw=lw/2., color=color, alpha=0.8)
            if output_label == "weighted":
                ax0.plot([0.081, 1], [prs_print/np.max(atm.p/1e+5), prs_print/np.max(atm.p/1e+5)], ls="--", lw=lw/2., color=color, alpha=0.8)

            photosphere[subdir+"_prs_norm"] = prs_print/np.max(atm.p/1e+5)
            photosphere[subdir+"_z"]        = z_print
            photosphere[subdir+"_prs_bar"]  = prs_print

            # Adjust x-axis right
            xmax = np.amax([np.max(cff_tot), xmax])

            # If smoothing
            if nsmooth > 1:
                cff_tot = np.convolve(cff_tot, np.ones((nsmooth,))/nsmooth, mode='valid')
                prs     = np.convolve(prs, np.ones((nsmooth,))/nsmooth, mode='valid')


            # Define data files
            data_file_cff = '../data/fig8_cff/'+str(subdir)+"_cff.txt"

            if os.path.isfile(data_file_cff):

                prs         = []
                cff_tot     = []
                cff_2       = []
                cff_6       = []
                cff_10      = []
                cff_lambda  = {}

                print("Read:", data_file_cff)

                with open(data_file_cff, "r") as filestream:
                    next(filestream) # skip header
                    filestream = [line.rstrip('\n') for line in filestream]
                    for line in filestream:
                        print(line)
                        data_values = line.split(" ")
                        cff_tot.append(float(data_values[0]))
                        prs.append(float(data_values[1]))
                        cff_2.append(float(data_values[2]))
                        cff_6.append(float(data_values[3]))
                        cff_10.append(float(data_values[4]))

                cff_lambda["2"]     = cff_2
                cff_lambda["6"]     = cff_6
                cff_lambda["10"]    = cff_10

            else:
                cff_lambda = {}
        

            # PLOT THE CFF
            # l1, = ax0.semilogy(atm.cff/np.sum(atm.cff), atm.p/np.max(atm.p), ls=ls, lw=lw, color=color, label=label_a)
            l1, = ax0.semilogy(cff_tot, prs, ls=ls, lw=lw, color=color, label=label_a)
            legend_ax0_handles.append(l1)

            wavelength_bands = [ 2, 6, 10 ] # microns

            

            for w_idx, wavelength in enumerate(wavelength_bands):

                if w_idx == 0:
                    lw = 1.5
                    ls = "-"
                if w_idx == 1:
                    lw = 1.5
                    ls = "--"
                if w_idx == 2:
                    lw = 1.5
                    ls = ":"
                if w_idx == 3:
                    lw = 1.5
                    ls = "-."
                if w_idx == 4:
                    lw = 1.5
                    ls = (0, (2, 1))

                if wavelength == 1.65:
                    band_name = r"$H$"
                elif wavelength == 2:
                    band_name = r"$K$"
                elif wavelength == 3.55:
                    band_name = r"$L$"
                elif wavelength == 10:
                    band_name = r"$N$"
                else:
                    band_name = "?"

                wavenumber = (1./wavelength)*1e+4 # cm

                label_b = vol_latex[subdir]+", "+str(round(wavelength, 1))+" $\mu$m"#+band_name

                channel, channel_idx = find_nearest(atm.band_centres, wavenumber )

                print(wavenumber, w_idx, wavelength, channel, channel_idx)
                print(subdir, sub_dirs[0])

                if os.path.isfile(data_file_cff):

                    # print(cff_lambda)

                    cff_band = cff_lambda[str(wavelength)]

                else:

                    # CFF per band
                    cff_band = atm.cff_i[channel_idx,:]/np.sum(atm.cff_i[channel_idx,:])
                    prs     = atm.p/np.max(atm.p)

                    # If smoothing
                    if nsmooth > 1:
                        cff_band = np.convolve(cff_band, np.ones((nsmooth,))/nsmooth, mode='valid')
                        prs     = np.convolve(prs, np.ones((nsmooth,))/nsmooth, mode='valid')

                    cff_lambda[str(wavelength)] = cff_band.tolist()

                l2, = ax1.semilogy(cff_band, prs, ls=ls, lw=lw, color=color, label=label_b) # 
                legend_ax1_handles.append(l2)

                # Dummy legend
                if subdir == sub_dirs[0]:
                    dummy, = ax1.semilogy([0], [0], ls=ls, lw=lw, color="k", label=str(round(wavelength, 1))+" $\mu$m") 
                    legend_ax1_dummy_handles.append(dummy)

            print(cff_lambda)

            if not os.path.isfile(data_file_cff):

                ## Write to file
                with open(data_file_cff, 'a') as data_file:
                    data_file.write("# P CFF_tot CFF_2 CFF_6 CFF_10\n")
                    for idx, cff in enumerate(cff_tot):
                        data_file.write(str(cff)+" "+str(prs[idx])+" "+str(cff_lambda["2"][idx])+" "+str(cff_lambda["6"][idx])+" "+str(cff_lambda["10"][idx])+"\n")

            # print(atm.cff)
            # print(np.shape(atm.cff), np.shape(atm.LW_flux_up))
            print("CFFs: ", np.sum(atm.cff), np.sum( atm.cff_i[:,:] ), atm.LW_flux_up[0], atm.net_flux[0])
            cff_sum = np.sum( atm.cff_i[:,:] * atm.LW_flux_up_i[:,0][:,None], axis=0)
            cff_sum = cff_sum / np.trapz(cff_sum, atm.p/np.max(atm.p), axis=0)
            print(np.sum(cff_sum), atm.LW_flux_up[0])

    if not os.path.isfile(data_file_photosphere):
        a_file = open(data_file_photosphere, "w")
        json.dump(photosphere, a_file)
        a_file.close()

    ax0.set_xlabel( r'Normalized flux contribution, $\mathcal{CF}_\mathrm{F}$ (non-dim.)', fontsize=fs_label )
    ax0.invert_yaxis()
    ax0.set_ylabel( 'Atmospheric pressure, $P/P_{\mathrm{surf}}$ (non-dim.)', fontsize=fs_label )
    ax0.set_ylim(bottom=1, top=1e-5) # , top=1e-5
    ax0.set_xlim(left=0, right=xmax)

    ax1.set_xlabel( r'Normalized flux contribution per band, $\mathcal{CF}_\mathrm{F}^{\nu}$ (non-dim.)', fontsize=fs_label )
    ax1.invert_yaxis()
    # ax1.set_yticklabels([])
    ax1.set_ylim(bottom=1, top=1e-5) # , top=1e-5
    
    try:
        sns.set_style("ticks")
        sns.despine()
    except:
        print("No seaborn.")

    # # Legend(s)
    legend_ax0 = ax0.legend(handles=legend_ax0_handles, loc=1, ncol=1, fontsize=fs_legend, framealpha=0.99, title=r"Volatile: $z$, $p$ weighted by $\mathcal{CF}_\mathrm{F}$") # , time $t$"
    ax0.add_artist(legend_ax0)
    
    # # Detailed legend
    # legend_ax1 = ax1.legend(handles=legend_ax1_handles, loc=[0.47, 0.1], ncol=2, fontsize=fs_legend, framealpha=0.3, title=r"Volatile species, wavelength $\lambda_\mathrm{c}$" )
    # ax1.add_artist(legend_ax1)

    # Only wavelengths legend
    legend_dummy = ax1.legend(handles=legend_ax1_dummy_handles, loc=1, ncol=1, fontsize=fs_legend, framealpha=0.3, title=r"Wavelength $\lambda$" )
    ax1.add_artist(legend_dummy)

    # ax2.text(0.6, 0.28, 'Mush', color=qmagenta_light, rotation=0, ha="left", va="top", fontsize=fs_label, transform=ax2.transAxes, bbox=dict(fc='white', ec="white", alpha=0.01, pad=0.1, boxstyle='round'))
    # ax2b.text(0.6, 0.28, 'Mush', color=qmagenta_light, rotation=0, ha="left", va="top", fontsize=fs_label, transform=ax2b.transAxes, bbox=dict(fc='white', ec="white", alpha=0.01, pad=0.1, boxstyle='round'))
    
    ax0.text(0.98, 0.015, 'A', color="k", rotation=0, ha="right", va="bottom", fontsize=fs_label+4, transform=ax0.transAxes, bbox=dict(fc='white', ec="white", alpha=0.01, pad=0.1, boxstyle='round'))
    ax1.text(0.98, 0.015, 'B', color="k", rotation=0, ha="right", va="bottom", fontsize=fs_label+4, transform=ax1.transAxes, bbox=dict(fc='white', ec="white", alpha=0.01, pad=0.1, boxstyle='round'))

    ax0.text(0.995, 0.31, r'$\mathcal{CF}_\mathrm{F}$–weighted'+'\n'+'photosphere', color="k", rotation=0, ha="right", va="bottom", fontsize=fs_legend, transform=ax0.transAxes, bbox=dict(fc='white', ec="white", alpha=0.01, pad=0.1, boxstyle='round'))

    # ax1.invert_xaxis()
    # ax1.yaxis.tick_right()
    # sns.despine(left=True, right=False)

    # ax0.legend( fancybox=True, framealpha=0.5, ncol=1, fontsize=fs_legend)
    # ax2.legend( fontsize=8, fancybox=True, framealpha=0.5 )
    plt.savefig('../figures/fig_8.pdf', tight_layout=True)

    # fig_o.savefig(1)
    plt.close()

#====================================================================
def main():

    # Optional command line arguments for running from the terminal
    # Usage: $ python plot_atmosphere.py -t 0,718259
    parser = argparse.ArgumentParser(description='COUPLER plotting script')
    parser.add_argument('-odir', '--output_dir', type=str, help='Full path to output directory');
    parser.add_argument('-t', '--times', type=str, help='Comma-separated (no spaces) list of times');
    args = parser.parse_args()

    # Define output directory for plots
    if args.output_dir:
        output_dir = args.output_dir
        print("Output directory:", output_dir)
        
    else:
        output_dir = os.getcwd()
        print("Output directory:", output_dir)

    # # Define which times are plotted
    # if args.times:
    #     data_times = [ int(time) for time in args.times.split(',') ]
    #     print("Snapshots:", output_times)
    # else:
    #     data_times = su.get_all_output_times(output_dir)
    #     print("Snapshots:", output_times)

    vols    = [ "H2", "H2O", "CO2", "CH4", "O2", "N2", "CO" ]
    # vols    = [ "CH4" ]

    output_dir  = "../data/int_atm/coupler_runs/"
    
    print("Host directory:", output_dir)

    # Plot fixed set from above
    plot_atmosphere( output_dir=output_dir, sub_dirs=vols )

#====================================================================

if __name__ == "__main__":

    # Import utils- and plot-specific modules
    from modules_utils import *
    from modules_plot import *
    import utils_coupler as cu
    import utils_spider as su

    main()