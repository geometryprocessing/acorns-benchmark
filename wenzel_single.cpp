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
   typedef Eigen::Matrix<double, 5, 1> Gradient;

   string output_filename = argv[1];
   cout << output_filename << endl;

   typedef DScalar1<double, Gradient> DScalar;

   int num_params = 70010;
   int num_vars = 5;

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
       DiffScalarBase::setVariableCount(5);
		DScalar a(0, args[index * 5 + 0]), b(1, args[index * 5 + 1]), c(2, args[index * 5 + 2]), d(3, args[index * 5 + 3]), e(4, args[index * 5 + 4]);
		DScalar Fx = (a) / (b) * (a) * (b * b) - (b) / (b * b) / (c * c) + (e * e) - (a) / (d * d) - (e) * (a) - (c) - (c * c) * (d) / (d * d) / (a * a) / (d * d) / (e * e) - (b);
		ders[index * 5 + 0] = Fx.getGradient()(0);
		ders[index * 5 + 1] = Fx.getGradient()(1);
		ders[index * 5 + 2] = Fx.getGradient()(2);
		ders[index * 5 + 3] = Fx.getGradient()(3);
		ders[index * 5 + 4] = Fx.getGradient()(4);
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