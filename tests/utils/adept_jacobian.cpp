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

   int num_params = 90010;
   int num_vars = 10;

   Stack stack;
   aVector  J(num_params), T(num_params), k(num_params), a(num_params), h(num_params), v(num_params), s(num_params), r(num_params), N(num_params), e(num_params);

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
			J(index) = args[index * num_vars + 0];
			T(index) = args[index * num_vars + 1];
			k(index) = args[index * num_vars + 2];
			a(index) = args[index * num_vars + 3];
			h(index) = args[index * num_vars + 4];
			v(index) = args[index * num_vars + 5];
			s(index) = args[index * num_vars + 6];
			r(index) = args[index * num_vars + 7];
			N(index) = args[index * num_vars + 8];
			e(index) = args[index * num_vars + 9];
    }


   ofstream outfile;
   outfile.open(output_filename);

   auto start = high_resolution_clock::now();
   stack.new_recording();                 // Clear any existing differential statements
   aReal J = 4*4*4*4*4*4*4*4*4*4*((sum(J * (1 - J)))*(sum(T * (1 - T)))*(sum(k * (1 - k)))*(sum(a * (1 - a)))*(sum(h * (1 - h)))*(sum(v * (1 - v)))*(sum(s * (1 - s)))*(sum(r * (1 - r)))*(sum(N * (1 - N)))*(sum(e * (1 - e))));
   J.set_gradient(1.0);                   // Seed the dependent variable
   stack.reverse();                       // Reverse-mode differentiation

   auto stop = high_resolution_clock::now();
   auto duration = duration_cast<microseconds>(stop - start);
   outfile << (double)duration.count() / 1000000.0 << " ";
   for (int index = 0; index < num_params; index++) {
			ders[index * num_vars + 0] = J.get_gradient()[index];
			ders[index * num_vars + 1] = T.get_gradient()[index];
			ders[index * num_vars + 2] = k.get_gradient()[index];
			ders[index * num_vars + 3] = a.get_gradient()[index];
			ders[index * num_vars + 4] = h.get_gradient()[index];
			ders[index * num_vars + 5] = v.get_gradient()[index];
			ders[index * num_vars + 6] = s.get_gradient()[index];
			ders[index * num_vars + 7] = r.get_gradient()[index];
			ders[index * num_vars + 8] = N.get_gradient()[index];
			ders[index * num_vars + 9] = e.get_gradient()[index];
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