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
   typedef Eigen::Matrix<double, 5, 5> Hessian;

   string output_filename = argv[1];
   cout << output_filename << endl;

   typedef DScalar2<double, Gradient, Hessian> DScalar;

   int num_params = 70010;
   int num_vars = 5;
   int num_ders = (num_vars * (num_vars + 1)) / 2;

   Eigen::VectorXd args(num_params * num_vars);
   Eigen::VectorXd ders(num_params * num_ders);

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
		ders[index * 15 + 0] = Fx.getHessian()(0);
		ders[index * 15 + 1] = Fx.getHessian()(1);
		ders[index * 15 + 2] = Fx.getHessian()(2);
		ders[index * 15 + 3] = Fx.getHessian()(3);
		ders[index * 15 + 4] = Fx.getHessian()(4);		ders[index * 15 + 5] = Fx.getHessian()(5);
		ders[index * 15 + 6] = Fx.getHessian()(6);
		ders[index * 15 + 7] = Fx.getHessian()(7);
		ders[index * 15 + 8] = Fx.getHessian()(8);
		ders[index * 15 + 9] = Fx.getHessian()(9);
		ders[index * 15 + 10] = Fx.getHessian()(10);
		ders[index * 15 + 11] = Fx.getHessian()(11);
		ders[index * 15 + 12] = Fx.getHessian()(12);
		ders[index * 15 + 13] = Fx.getHessian()(13);
		ders[index * 15 + 14] = Fx.getHessian()(14);

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