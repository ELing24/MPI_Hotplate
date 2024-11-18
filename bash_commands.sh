#!/bin/bash -l

#SBATCH --job-name=mpi_job
#SBATCH --partition=batch
#SBATCH --nodes=2 # Allocate *at least* 5 nodes (5 nodes in the batch queue)
#SBATCH --time=00:05:00 # 5 minutes
#SBATCH --wait-all-nodes=1  # Run once all resources are available
#SBATCH --output=mpi_job_%j.txt # Standard output and error are logged
echo "Number of allocated nodes: $SLURM_JOB_NUM_NODES"
echo "Allocated nodes: $SLURM_JOB_NODELIST"
# Load any necessary modules here
module load mpi/openmpi-x86_64
#compile hotplate
mpicxx -o hotplate hotplate.cpp
# Run the MPI program -n 2
mpirun -n 2 ./hotplate 200 10 10 10 10 10 100 100 100 10 1000 output.dat
python3 heatmap.py --data=output.dat --png=pretty.png

#mpicxx -o hotplate hotplate.cpp
#sbatch bash_commands.sh
#squeue -u $USER