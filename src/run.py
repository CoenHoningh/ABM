import modelgrid

mod1 = modelgrid.RoadSim(lanes=2)

# mod1.visualise()

mod1.run_sim(steps=5000)