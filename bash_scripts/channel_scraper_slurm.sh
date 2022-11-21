#!/bin/bash
# 20220409 Generic job script for XBOX data projects on spartan. 
# AUTHOR: Paarangat Pushkarna

#SBATCH --partition=physical
#SBATCH --nodes=1
#SBATCH --job-name="scraping_test"
#SBATCH --account="punim1158"
#SBATCH --ntasks=1
#SBATCH --time=0-3:00:00
#SBATCH --array=1-383
#SBATCH --cpus-per-task=5

module purge
module load gcccore/10.3.0
module load python/3.9.5

HOME="/data/gpfs/projects/punim1158/pushkarnap"
source /home/pushkarnap/virtualenv/mlfram20220408/bin/activate
export PYTHONPATH="${PYTHONPATH}:${HOME}/rfstudies/"
echo "Starting task $SLURM_ARRAY_TASK_ID"
item=$(sed -n "${SLURM_ARRAY_TASK_ID}p" filelist_bol3.txt)

DATA="/xbox3_td24_20182020/a_bo_l3"
SCRIPTS="/scraping_code"
OUT="/scraped_data/xbox3_td24bol3_data"
# LAUNCH YOUR PYTHON SCRIPTS HERE!

python "${HOME}${SCRIPTS}/scrape_channel_spartan.py" -f "${HOME}${DATA}/${item}" \
-c "${HOME}${OUT}/xbox3_td24bol3_U_INC.csv" \
-p "PSI_amp" \
-s "get_pulse_energy" \
-n "U_INC" &

python "${HOME}${SCRIPTS}/scrape_channel_spartan.py" -f "${HOME}${DATA}/${item}" \
-c "${HOME}${OUT}/xbox3_td24bol3_U_TRA.csv" \
-p "PEI_amp" \
-s "get_pulse_energy" \
-n "U_TRA" &

python "${HOME}${SCRIPTS}/scrape_channel_spartan.py" -f "${HOME}${DATA}/${item}" \
-c "${HOME}${OUT}/xbox3_td24bol3_U_REF.csv" \
-p "PSR_amp" \
-s "get_pulse_energy" \
-n "U_REF" &

python "${HOME}${SCRIPTS}/scrape_channel_spartan.py" -f "${HOME}${DATA}/${item}" \
-c "${HOME}${OUT}/xbox3_td24bol3_amp.csv" \
-p "PSI_amp" \
-s "get_pulse_meanamp" \
-n "INC_MeanAmp" &

python "${HOME}${SCRIPTS}/scrape_channel_spartan.py" -f "${HOME}${DATA}/${item}" \
-c "${HOME}${OUT}/xbox3_td24bol3_pw.csv" \
-p "PSI_amp" \
-s "get_PulseWidth" \
-n "INC_MeanAmp" &

my-job-stats -a -n -s
