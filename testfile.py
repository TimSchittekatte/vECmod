# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 12:37:06 2016

@author: tschitte
"""

from pyomo.environ import *
from pyomo.bilevel import *
from collections import Counter

model= ConcreteModel()
model.sub=SubModel()

# adding another variable to the subproblem
model.x=Var(bounds=(1,2))
model.v=Var(bounds=(1,2))
model.sub.y=Var(bounds=(1,2))
model.sub.w=Var(bounds=(-1,1))
model.sub.tim=Var(bounds(0,10))
model.sub.ilan=Var(bounds(-5,5))

model.o=Objective(expr=model.x +model.sub.y+model.v)
model.c=Constraint(expr=model.x+model.x >= 1.5)

# adding a constraint to the problem
model.sub.o=Objective(expr=model.x+model.sub.w+model.sub.tim, sense=maximize)
model.sub.c=Constraint(expr=model.sub.y+ model.sub.w <=2.5)
model.sub.con=Constraint(expr=model.sub.w+ model.sub.l <=8)  #chekc this out.

xfrm= TransformationFactory('bilevel.linear_mpec')
xfrm.apply_to(model)

opt = SolverFactory('cplex')
instance = model.create_instance()
results = opt.solve(instance, tee=False, load_solutions=False)
instance.solutions.load_from(results)
results.write()
