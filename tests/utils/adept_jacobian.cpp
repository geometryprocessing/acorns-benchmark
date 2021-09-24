#include <iostream>
#include <fstream>
#include <string>
#include <Eigen/Cholesky>
#include <adept_arrays.h>
#include <chrono>

using namespace adept;
using namespace std;
using namespace std::chrono;
int main(int argc, char **argv)
{
   string output_filename = argv[1];
   cout << output_filename << endl;

   int num_params = 4010;
   int num_vars = 1;

   Stack stack;
   aVector  k(num_params);

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


   for (int index = 0; index < num_params; index++) {
			k(index) = args[index * num_vars + 0];
    }


   ofstream outfile;
   outfile.open(output_filename);

   auto start = high_resolution_clock::now();
   stack.new_recording();                 // Clear any existing differential statements
   aReal J = sum(((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k);
   J.set_gradient(1.0);                   // Seed the dependent variable
   stack.reverse();                       // Reverse-mode differentiation

   auto stop = high_resolution_clock::now();
   auto duration = duration_cast<microseconds>(stop - start);
   outfile << (double)duration.count() / 1000000.0 << " ";
   for (int index = 0; index < num_params; index++) {
			ders[index * num_vars + 0] = k.get_gradient()[index];
    }
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