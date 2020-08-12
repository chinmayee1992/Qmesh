Notes: 
After running the script for global mesh,lining issue occurs due to folding of data.It can be solved by running the following command in the Ubantu terminal after tweaking the raster mesh metric resolution(1000,900).
             
                         "gmsh -2 algo del2d simplistic_earth.geo -format vtk"

'del2d'(Dealunary) is the algorith that has been used in this case. Apart from this other algorithms like Mesh Adapt,Frontal can be used.
     
               


