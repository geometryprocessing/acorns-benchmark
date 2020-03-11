#include <iostream>
#include <fstream>
#include <string>
#include <Eigen/Cholesky>
#include "autodiff.h"
#include <chrono>

DECLARE_DIFFSCALAR_BASE();
using namespace std;
using namespace std::chrono;
int main(int argc, char **argv)
{
   typedef Eigen::Matrix<double, 9, 1> Gradient;

   string output_filename = argv[1];
   cout << output_filename << endl;

   typedef DScalar1<double, Gradient> DScalar;

   int num_params = 8010;
   int num_vars = 9;

   Eigen::VectorXd args(num_params * num_vars);
   Eigen::VectorXd ders(num_params * num_vars);

   std::ifstream file("utils/params.txt");
   int i = 0;
   for (std::string line; std::getline(file, line);)
   {
       args(i) = stod(line.c_str());
       i++;
   }
   file.close();

   ofstream outfile;
   outfile.open(output_filename);

   auto start = high_resolution_clock::now();
   for (int index = 0; index < num_params; index++)
   {
       /* There are two independent variables */
       DiffScalarBase::setVariableCount(9);
		DScalar d(0, args[index * 9 + 0]), E(1, args[index * 9 + 1]), J(2, args[index * 9 + 2]), c(3, args[index * 9 + 3]), x(4, args[index * 9 + 4]), X(5, args[index * 9 + 5]), u(6, args[index * 9 + 6]), O(7, args[index * 9 + 7]), P(8, args[index * 9 + 8]);
		DScalar Fx = 4*4*4*4*4*4*4*4*4*((d * (1 - d))*(E * (1 - E))*(J * (1 - J))*(c * (1 - c))*(x * (1 - x))*(X * (1 - X))*(u * (1 - u))*(O * (1 - O))*(P * (1 - P)));
		ders[index * 9 + 0] = Fx.getGradient()(0);
		ders[index * 9 + 1] = Fx.getGradient()(1);
		ders[index * 9 + 2] = Fx.getGradient()(2);
		ders[index * 9 + 3] = Fx.getGradient()(3);
		ders[index * 9 + 4] = Fx.getGradient()(4);
		ders[index * 9 + 5] = Fx.getGradient()(5);
		ders[index * 9 + 6] = Fx.getGradient()(6);
		ders[index * 9 + 7] = Fx.getGradient()(7);
		ders[index * 9 + 8] = Fx.getGradient()(8);
   }

   auto stop = high_resolution_clock::now();
   auto duration = duration_cast<microseconds>(stop - start);
   outfile << (double)duration.count() / 1000000.0 << " ";
   for (int i = 0; i < num_params * num_vars; i++)
   {
       outfile << ders[i] << " ";
   }

   outfile.close();

   return 0;
}