#include <iostream>
#include <fstream>
#include <string>
#include <Eigen/Cholesky>
#include "../headers/autodiff.h"
#include <chrono>

DECLARE_DIFFSCALAR_BASE();
using namespace std;
using namespace std::chrono;
int main(int argc, char **argv)
{
   typedef Eigen::Matrix<double, 10, 1> Gradient;

   string output_filename = argv[1];
   cout << output_filename << endl;

   typedef DScalar1<double, Gradient> DScalar;

   int num_params = 90010;
   int num_vars = 10;

   Eigen::VectorXd args(num_params * num_vars);
   Eigen::VectorXd ders(num_params * num_vars);

   std::ifstream file("./tests/utils/params.txt");
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
       DiffScalarBase::setVariableCount(10);
		DScalar J(0, args[index * 10 + 0]), T(1, args[index * 10 + 1]), k(2, args[index * 10 + 2]), a(3, args[index * 10 + 3]), h(4, args[index * 10 + 4]), v(5, args[index * 10 + 5]), s(6, args[index * 10 + 6]), r(7, args[index * 10 + 7]), N(8, args[index * 10 + 8]), e(9, args[index * 10 + 9]);
		DScalar Fx = 4*4*4*4*4*4*4*4*4*4*((J * (1 - J))*(T * (1 - T))*(k * (1 - k))*(a * (1 - a))*(h * (1 - h))*(v * (1 - v))*(s * (1 - s))*(r * (1 - r))*(N * (1 - N))*(e * (1 - e)));
		ders[index * 10 + 0] = Fx.getGradient()(0);
		ders[index * 10 + 1] = Fx.getGradient()(1);
		ders[index * 10 + 2] = Fx.getGradient()(2);
		ders[index * 10 + 3] = Fx.getGradient()(3);
		ders[index * 10 + 4] = Fx.getGradient()(4);
		ders[index * 10 + 5] = Fx.getGradient()(5);
		ders[index * 10 + 6] = Fx.getGradient()(6);
		ders[index * 10 + 7] = Fx.getGradient()(7);
		ders[index * 10 + 8] = Fx.getGradient()(8);
		ders[index * 10 + 9] = Fx.getGradient()(9);
   }

   auto stop = high_resolution_clock::now();
   auto duration = duration_cast<microseconds>(stop - start);
   outfile << (double)duration.count() / 1000000.0 << " ";
   for (int i = 0; i < num_params * num_vars; i++)
   {
        ostringstream ss;
        ss.precision(3);
       ss << fixed << ders[i];
       outfile << ss.str() << " ";
   }

   outfile.close();

   return 0;
}