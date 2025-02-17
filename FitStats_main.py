from FitStats_aux import load_data, plot_avg_records
import sys

if __name__ == "__main__":
	# Load data:
	FilePath = r"../Downloads/2025-2020 Control Ejercicio.xlsx" # Path for original data file
	t_card, t_abs, t_total, Dates, Obs_abs, Obs_card = load_data(FilePath) # [min,min,min,str,str,str]
	print(f"Last registry: {Dates[-1]}")

	# Identify variables for plots, from the terminal:
	# Command format is: python3 FitStats_main.py quarterly moonly weekly daily
	last_years_quarterly = int(sys.argv[1]) if len(sys.argv)>1 else -1
	last_years_moonly = int(sys.argv[2]) if len(sys.argv)>2 else -1
	last_years_weekly = int(sys.argv[3]) if len(sys.argv)>3 else 2
	last_years_daily = int(sys.argv[4]) if len(sys.argv)>4 else 1

	# Plot results:
	plot_avg_records(t_total,t_card,t_abs,Dates,quarterly=True,last_years=last_years_quarterly)
	plot_avg_records(t_total,t_card,t_abs,Dates,moonly=True,last_years=last_years_moonly)
	plot_avg_records(t_total,t_card,t_abs,Dates,weekly=True,last_years=last_years_weekly)
	plot_avg_records(t_total,t_card,t_abs,Dates,daily=True,last_years=last_years_daily)
	#plot_effec_dist(t_total,t_card,t_abs)