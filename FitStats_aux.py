# Libraries:
import pandas as pd
import numpy as np
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
import matplotlib.dates

# Plot configuration:
wPlot = 16                      # Default width for figures
hPlot = 5                       # Default height for figures
Color_abs = "#0F52BA"          # Main color for figures
Color_cardio = "#EF7215"
Color_total = "#4CBB17"
plt.rc('legend', fontsize=14)   # Fontsize of legends
plt.rc('figure', titlesize=20)  # Fontsize of the figure title
plt.rc('xtick', labelsize=16)   # Fontsize for the xtick-labels
plt.rc('ytick', labelsize=16)   # Fontsize for the ytick-labels
plt.rc('axes', labelsize=18)    # Fontsize of the x and y labels

def load_data(FilePath):
    """
    Xxxx
    """
    # Read data:
    File = pd.read_excel(FilePath)      # Pandas dataframe; Read file
    Data = File.to_dict('list')         # Dictionary; Condense all information to Python format
    t_card = np.array(Data['t cardio [min]'])  # Numpy array; Time for any other exercise [min]
    LastEntry = np.argwhere(np.isnan(t_card))[0][0]  # Identify the last valid entry for all lists
    t_card = t_card[:LastEntry]     # Keep only valid rows
    Dates = Data['FECHA'][:LastEntry]                  # List; Dates list
    Days = np.array(Data['DÍA'][:LastEntry])          # Numpy array; Days (starts in 1)
    t_abs = np.array(Data['t abs [min]'][:LastEntry]) # Numpy array; Time for abs [min]
    Obs_abs = Data['Obs abs'][:LastEntry]             # List; Observations for abs    
    Obs_card = Data['Obs cardio'][:LastEntry]       # Observations for any other exercise

    # Fix date entries:
    for i in range(len(Dates)):                     # Go thorugh all entries
        if Dates[i] != Dates[i]:                    # Correct NaT entries
            Dates[i] = Dates[i-1] + timedelta(1)
    # Convert dates to dates format:
    time_format = "%d/%m/%Y"                        # String format for dates
    Dates = [date.strftime(time_format) for date in Dates]

    # Calculate total time list from abs and cardio:
    t_total = t_abs + t_card                       # Numpy array; Total exercise time [min]

    return t_card, t_abs, t_total, Dates, Obs_abs, Obs_card

def plot_effec_dist(t_total,t_card,t_abs):
    """
    Xxx
    """
    N = len(t_total) # Number of data entries
    
    #Calculate effectivity:
    ef_only_abs = round(sum([t_abs[i]>0 and t_card[i]==0 for i in range(N)])/N*100,1) # Only abs days [%]
    ef_only_card = round(sum([t_abs[i]==0 and t_card[i]>0 for i in range(N)])/N*100,1) # Only abs days [%]
    ef_both = round(sum([t_abs[i]>0 and t_card[i]>0 for i in range(N)])/N*100,1) # Only abs+cardio days [%]
    ef_none = 100-ef_only_card-ef_both-ef_only_abs # No exercise [%]
    
    # Calculate average activity for each day of the week:
    week_days = ['Friday', 'Saturday', 'Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday']
    week_day_abs = [np.mean(t_abs[i::7]) for i in range(7)] # Average exercise for abs [min]
    week_day_card = [np.mean(t_card[i::7]) for i in range(7)] # Average exercise for cardio [min]

    # Generate plot for exercise effectivity and distribution:
    fig, (ax_efec,ax_dist) = plt.subplots(1,2,figsize=(wPlot,hPlot),constrained_layout=True,
                                          gridspec_kw={'width_ratios': [1, 2]})
    # Effectivity:
    e = [0.02,0.02,0.02,0.15]       # Explode parameter
    Colors = [Color_abs, Color_cardio, Color_total, 'gray']    # Colors
    effectivity = np.array([ef_only_abs,ef_only_card,ef_both,ef_none])    # Data [%]
    Label = ['Abs','Cardio','Both','Nothing'] 
    ax_efec.set_title(f'Distribution of {N} exercise days \n',fontsize=16)
    patches,texts,autotexts = ax_efec.pie(effectivity, labels=Label, colors=Colors, explode=e, 
                                      autopct=lambda x:'{:.0f}%'.format(x),
                                      startangle=30, shadow=True)
    counterAux = 0
    for text in texts:
        text.set_color(Colors[counterAux])
        text.set_fontsize(18)
        counterAux += 1
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
    ax_efec.axis('equal')  
    
    # Weekdays distribution:
    #fig_WeekdaysAvg.suptitle('Weekdays averages')
    ax_dist.set_title(f'Weekdays averages (includes all {N} exercise days)',fontsize=16)
    ax_dist.set_facecolor("#3c3c3c")
    ax_dist.grid(axis='y',alpha=0.2)
    ax_dist.set_ylabel('Avg. Daily time [min]')
    ax_dist.bar(week_days, week_day_abs, label='Abs', color=Color_abs)
    ax_dist.bar(week_days, week_day_card, bottom=week_day_abs, label='Cardio', color=Color_cardio)
    ax_dist.set_xticklabels(week_days, rotation = 30, fontsize=15)
    ax_dist.legend(facecolor='wheat')
    plt.show()

def plot_avg_records(
	t_total,t_card,t_abs,Dates,
	daily=False,last_years_daily=1,
	weekly=False,last_years_weekly=1,
	moonly=False,last_years_moonly=1,
	quarterly=False,last_years_quarterly=1,
    ):
    """
    Xxx
    """
    if daily+weekly+moonly+quarterly==0:
        print('Choose either <daily>, <weekly>, <moonly> and/or <quarterly> equal True.')
    # Define time ranges:
    N_days = len(t_abs) # Number of days so far
    N_weeks = N_days//7 # Number of weeks so far
    N_moons = N_days//28 # Number of moons so far
    N_quarts = N_days//90 # Number of quarters so far
    # Calculate weekly averages:
    t_total_weekly = [np.mean(t_total[i*7:(i+1)*7]) for i in range(N_weeks)] # [min]
    t_card_weekly = [np.mean(t_card[i*7:(i+1)*7]) for i in range(N_weeks)] # [min]
    t_abs_weekly = [np.mean(t_abs[i*7:(i+1)*7]) for i in range(N_weeks)] # [min]
    date_weekly = [Dates[i*7+6] for i in range(N_weeks)] # Last day of each week
    # Calculate moonly averages:
    t_total_moonly = [np.mean(t_total[i*28:(i+1)*28]) for i in range(N_moons)] # [min]
    t_card_moonly = [np.mean(t_card[i*28:(i+1)*28]) for i in range(N_moons)] # [min]
    t_abs_moonly = [np.mean(t_abs[i*28:(i+1)*28]) for i in range(N_moons)] # [min]
    date_moonly = [Dates[i*28+27] for i in range(N_moons)] # Last day of each moon
    # Calculate quarterly averages:
    t_total_quart = [np.mean(t_total[i*90:(i+1)*90]) for i in range(N_quarts)] # [min]
    t_card_quart = [np.mean(t_card[i*90:(i+1)*90]) for i in range(N_quarts)] # [min]
    t_abs_quart = [np.mean(t_abs[i*90:(i+1)*90]) for i in range(N_quarts)] # [min]
    date_quart = [Dates[i*90+89][3:] for i in range(N_quarts)] # Last month of each quarter    
   
    # Plot figures:
    alpha_grid = 0.2
    n_plots = daily+weekly+moonly+quarterly
    if n_plots == 1:
    	fig, ax = plt.subplots(n_plots,1,figsize=(wPlot,hPlot*(n_plots)))
    	axes = [ax]
    else:
    	fig, axes = plt.subplots(n_plots,1,figsize=(wPlot,hPlot*(n_plots)),constrained_layout=True)
    i_aux = 0 # Start counter
    if daily:
        N_days = len(t_abs) if last_years_daily==-1 else int(last_years_daily*365) # Number of days to be plotted
        if N_days//15>15:
            N_spacing = N_days//15
        elif N_days//15>7:
            N_spacing = N_days//7
        else:
            N_spacing = 7
        axes[i_aux].grid(axis='y',alpha=alpha_grid)
        axes[i_aux].set_title("Daily series",fontsize=18,color='black')      
        axes[i_aux].bar(Dates[-N_days:],t_abs[-N_days:],label='Abs',color=Color_abs)
        axes[i_aux].bar(Dates[-N_days:],t_card[-N_days:],bottom=t_abs[-N_days:],label='Cardio',color=Color_cardio)
        DateLabel = Dates[-N_days::N_spacing] # Define date labels
        DaysTicks = [i*N_spacing for i in range(len(DateLabel))] # Adjust ticks accordingly
        axes[i_aux].set_facecolor("#000000")
        axes[i_aux].set_xticks(DaysTicks)
        axes[i_aux].set_xticklabels(DateLabel,rotation=30,fontsize=12)
        axes[i_aux].legend(facecolor='wheat',loc=2)
        axes[i_aux].set_ylabel('Avg. time [min]')
        i_aux += 1 # Update counter
        
    if weekly:
        N_weeks = len(t_abs)//7 if last_years_weekly==-1 else int(last_years_weekly*365//7) # Number of days to be plotted
        N_spacing = 4 if N_weeks/4<15 else N_weeks//15 # Separation between date labels
        axes[i_aux].grid(axis='y',alpha=alpha_grid)
        axes[i_aux].set_title("Weekly series",fontsize=18,color='black')      
        axes[i_aux].bar(date_weekly[-N_weeks:],t_abs_weekly[-N_weeks:],label='Abs',color=Color_abs)
        axes[i_aux].bar(date_weekly[-N_weeks:],t_card_weekly[-N_weeks:],bottom=t_abs_weekly[-N_weeks:],
               label='Cardio',color=Color_cardio)
        DateLabel = date_weekly[-N_weeks::N_spacing] # Define date labels
        WeekTicks = [i*N_spacing for i in range(len(DateLabel))] # Adjust ticks accordingly
        axes[i_aux].set_facecolor("#111111")
        axes[i_aux].set_xticks(WeekTicks)
        axes[i_aux].set_xticklabels(DateLabel,rotation=30,fontsize=12)
        axes[i_aux].legend(facecolor='wheat',loc=2)
        axes[i_aux].set_ylabel('Avg. time [min]')
        i_aux += 1 # Update counter
        
    if moonly:
        N_moons = len(t_abs)//28 if last_years_moonly==-1 else int(last_years_moonly*365//28) # Number of days to be plotted
        N_spacing = 1 if N_moons<15 else N_moons//15 # Separation between date labels
        axes[i_aux].grid(axis='y',alpha=alpha_grid)
        axes[i_aux].set_title("Moonly series",fontsize=18,color='black')      
        axes[i_aux].bar(date_moonly[-N_moons:],t_abs_moonly[-N_moons:],label='Abs',color=Color_abs)
        axes[i_aux].bar(date_moonly[-N_moons:],t_card_moonly[-N_moons:],bottom=t_abs_moonly[-N_moons:],
               label='Cardio',color=Color_cardio)
        DateLabel = date_moonly[-N_moons::N_spacing] # Define date labels
        MoonTicks = [i*N_spacing for i in range(len(DateLabel))] # Adjust ticks accordingly
        axes[i_aux].set_facecolor("#1e1e1e")
        axes[i_aux].set_xticks(MoonTicks)
        axes[i_aux].set_xticklabels(DateLabel,rotation=30,fontsize=12)
        axes[i_aux].legend(facecolor='wheat',loc=2)
        axes[i_aux].set_ylabel('Avg. time [min]')
        i_aux += 1 # Update counter
        
    if quarterly:
        N_quarts = len(t_abs)//90 if last_years_quarterly==-1 else int(last_years_quarterly*365//90) # Number of days to be plotted
        N_spacing = 1 if N_quarts<15 else N_quarts//15 # Separation between date labels
        axes[i_aux].grid(axis='y',alpha=alpha_grid)
        axes[i_aux].set_title("Quarterly series",fontsize=18,color='black')      
        axes[i_aux].bar(date_quart[-N_quarts:],t_abs_quart[-N_quarts:],label='Abs',color=Color_abs)
        axes[i_aux].bar(date_quart[-N_quarts:],t_card_quart[-N_quarts:],bottom=t_abs_quart[-N_quarts:],
               label='Cardio',color=Color_cardio)
        DateLabel = date_quart[-N_quarts::N_spacing] # Define date labels
        QuartTicks = [i*N_spacing for i in range(len(DateLabel))] # Adjust ticks accordingly
        axes[i_aux].set_facecolor("#1e1e1e")
        axes[i_aux].set_xticks(QuartTicks)
        axes[i_aux].set_xticklabels(DateLabel,rotation=30,fontsize=12)
        axes[i_aux].legend(facecolor='wheat',loc=2)
        axes[i_aux].set_ylabel('Avg. time [min]')
        i_aux += 1 # Update counter
        
    #fig.tight_layout()
    #plt.subplots_adjust(left=0.125, bottom=0.9, right=0.1, top=0.9, wspace=0.2, hspace=0.2)
    plt.show()

# Obtain averages in week_days:
def obtain_avg(input_list):
    """
    Obtains averages
    """
    avg = []
    for i in range(len(input_list)):
        avg.append(round(np.mean(input_list[i]),2))
    return avg

# Obtain standar deviation in week_days:
def obtain_std_dev(input_list):
    std_dev = []
    for i in range(len(input_list)):
        std_dev.append(round(np.std(input_list[i]),2))
    return std_dev