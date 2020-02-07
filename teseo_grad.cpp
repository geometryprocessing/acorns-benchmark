#include <math.h>
#include <vector>
#include <cassert>
#include <iostream>
#include "autodiff.h"
#include <Eigen/Cholesky>
#include <chrono>
#include <fstream>
#include <string>

using namespace std;
using namespace std::chrono;
DECLARE_DIFFSCALAR_BASE();

typedef Eigen::Matrix<double, 12, 1> Gradient;
typedef DScalar2<double, Gradient> DScalar;

template <typename T>
T determinant(const Eigen::Matrix<T, 3, 3> &mat);
DScalar func(const double *local_disp, const int local_disp_size, const double *grads, const int grads_size,
            const double *vjac_it, const int vjac_it_size, const double *da, const int da_size,
            const double mu, const double lambda, const int size);


int main(int argc, char const *argv[])
{
    ostringstream ss;
    ss.precision(3);

    std::vector<double> local_disp = {-295.38951896095, 6211.61997312979, 206.024220985328, -253.613449943513, 6321.61661016864, 49.7582549106343, -336.495776971934, 5994.1710790185, 60.5450561578149, -290.120487841469, 7528.84895092188, 56.3418291554071};
    std::vector<double> grads = {-1, -1, -1, 1, 0, 0, 0, 1, 0, 0, 0, 1, -1, -1, -1, 1, 0, 0, 0, 1, 0, 0, 0, 1, -1, -1, -1, 1, 0, 0, 0, 1, 0, 0, 0, 1, -1, -1, -1, 1, 0, 0, 0, 1, 0, 0, 0, 1, -1, -1, -1, 1, 0, 0, 0, 1, 0, 0, 0, 1, -1, -1, -1, 1, 0, 0, 0, 1, 0, 0, 0, 1, -1, -1, -1, 1, 0, 0, 0, 1, 0, 0, 0, 1, -1, -1, -1, 1, 0, 0, 0, 1, 0, 0, 0, 1, -1, -1, -1, 1, 0, 0, 0, 1, 0, 0, 0, 1, -1, -1, -1, 1, 0, 0, 0, 1, 0, 0, 0, 1, -1, -1, -1, 1, 0, 0, 0, 1, 0, 0, 0, 1};
    std::vector<double> vjac_it = {0.515346611872346, 0.461608323857631, -0.976954935729977, 0.424748849456088, -0.34091955936939, -0.0838292900866981, -0.216719409535271, -0.240960572494519, -0.0103658280285318, 0.515346611872346, 0.461608323857631, -0.976954935729977, 0.424748849456088, -0.34091955936939, -0.0838292900866981, -0.216719409535271, -0.240960572494519, -0.0103658280285318, 0.515346611872346, 0.461608323857631, -0.976954935729977, 0.424748849456088, -0.34091955936939, -0.0838292900866981, -0.216719409535271, -0.240960572494519, -0.0103658280285318, 0.515346611872346, 0.461608323857631, -0.976954935729977, 0.424748849456088, -0.34091955936939, -0.0838292900866981, -0.216719409535271, -0.240960572494519, -0.0103658280285318, 0.515346611872346, 0.461608323857631, -0.976954935729977, 0.424748849456088, -0.34091955936939, -0.0838292900866981, -0.216719409535271, -0.240960572494519, -0.0103658280285318, 0.515346611872346, 0.461608323857631, -0.976954935729977, 0.424748849456088, -0.34091955936939, -0.0838292900866981, -0.216719409535271, -0.240960572494519, -0.0103658280285318, 0.515346611872346, 0.461608323857631, -0.976954935729977, 0.424748849456088, -0.34091955936939, -0.0838292900866981, -0.216719409535271, -0.240960572494519, -0.0103658280285318, 0.515346611872346, 0.461608323857631, -0.976954935729977, 0.424748849456088, -0.34091955936939, -0.0838292900866981, -0.216719409535271, -0.240960572494519, -0.0103658280285318, 0.515346611872346, 0.461608323857631, -0.976954935729977, 0.424748849456088, -0.34091955936939, -0.0838292900866981, -0.216719409535271, -0.240960572494519, -0.0103658280285318, 0.515346611872346, 0.461608323857631, -0.976954935729977, 0.424748849456088, -0.34091955936939, -0.0838292900866981, -0.216719409535271, -0.240960572494519, -0.0103658280285318, 0.515346611872346, 0.461608323857631, -0.976954935729977, 0.424748849456088, -0.34091955936939, -0.0838292900866981, -0.216719409535271, -0.240960572494519, -0.0103658280285318};
    std::vector<double> da = {0.0375967432131164, 0.0529437174283588, 0.0530590712946449, 0.0574071323575205, 0.0665419586778496, 0.0729526232273157, 0.0760790190648713, 0.101980639167817, 0.105588100413444, 0.148444211377106, 0.185258968959474};
    double lambda = 0.32967032967033;
    double mu = 0.384615384615385;
    int size = 3;
    string output_filename = "./results/wenzel/grad/3D_P1_non_zero_grad.txt";

    Eigen::VectorXd ders(local_disp.size(), local_disp.size());

    auto start = high_resolution_clock::now();

    DScalar en = func(
        &local_disp[0], local_disp.size(),
        &grads[0], grads.size(),
        &vjac_it[0], vjac_it.size(),
        &da[0], da.size(),
        lambda, mu, size);

    Gradient grad = en.getGradient();
    Gradient &grad_ref = grad;

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    std::cout << en << endl;
    std::cout << "Time took: " << (double)duration.count() / 1000000.0 << endl;
    ofstream outfile;
    outfile.open(output_filename);
    outfile << (double)duration.count() / 1000000.0 << " ";

    double expected_value = 327331.435073887;
    assert(fabs(expected_value - en.getValue()) < 1e-8);

    std::vector<double> expected_grads = {0.1412,  2.57,  12.35,  4.592,  -252,  -6.657,  -4.324,  -229,  -6.074,  -0.4096,  478.5,  0.3793};
    for (int i = 0; i < grad_ref.size(); i++)
    {
        double current_grad = grad_ref(i);
        double expected_grad = expected_grads[i];
        // std::cout << "current_grad: " << current_grad << ", expected_grad: " << expected_grad << endl;
        assert(fabs(expected_grad - current_grad) < 1e-8);
    }

    /*
    for (int i = 0; i < local_disp.size() * local_disp.size(); i++)
    {
        ostringstream ss;
        ss.precision(3);
        ss << fixed << ders[i];
        outfile << ss.str() << " ";
    }
    */

    outfile.close();
    return 0;
}

/*
local_disp: n_local_disp x size (3)
grads: n_pts x n_grads x size (3)
vjac_it: n_pts x size x size (3)
da: n_pts x 1
*/
DScalar func(const double *local_disp, const int local_disp_size, const double *grads,
            const int grads_size, const double *vjac_it, const int vjac_it_size,
            const double *da, const int da_size, const double lambda, const double mu, const int size)
{

    std::cout << "local_disp_size: " << local_disp_size << endl;
    typedef Eigen::Matrix<DScalar, 12, 1> AutoDiffVect;
    typedef Eigen::Matrix<DScalar, 3, 3> AutoDiffGradMat;

    DiffScalarBase::setVariableCount(local_disp_size);
    int n_local_disp = local_disp_size / size; 
    int n_grads = grads_size / da_size / size; 
    assert(n_grads == n_local_disp);
    int n_pts = da_size;

    DScalar energy = DScalar(0.0);

    AutoDiffVect local_disp_ad;

    for (long i = 0; i < local_disp_size; ++i)
    {
        local_disp_ad(i) = DScalar(i, local_disp[i]);
    }

    AutoDiffGradMat def_grad;

    for (long p = 0; p < n_pts; ++p)
    {

        for (long k = 0; k < def_grad.size(); ++k)
        {
            def_grad(k) = DScalar(0.0);
        }

        for (int i = 0; i < n_grads; ++i)
        {
            for (int d = 0; d < size; ++d)
            {
                for (int c = 0; c < size; ++c)
                {
                    assert(i * size + d < local_disp_size);
                    assert((i + p * n_grads) * size + c < grads_size);
                    def_grad(d, c) += DScalar(grads[(i + p * n_grads) * size + c]) * local_disp_ad(i * size + d);
                }
            }
        }

        AutoDiffGradMat jac_it;
        for (long k = 0; k < jac_it.size(); ++k)
            jac_it(k) = DScalar(vjac_it[k]);

        def_grad = def_grad * jac_it;

        //Id + grad d
        for (int d = 0; d < size; ++d)
            def_grad(d, d) += DScalar(1.0);

        DScalar log_det_j = log(determinant(def_grad));
        DScalar val = mu / 2. * ((def_grad.transpose() * def_grad).trace() - size - 2 * log_det_j) + lambda / 2. * log_det_j * log_det_j;
        energy += val * DScalar(da[p]);
    }

    return energy;
}

template <typename T>
T determinant(const Eigen::Matrix<T, 3, 3> &mat)
{
    assert(mat.rows() == mat.cols());

    if (mat.rows() == 1)
        return mat(0);
    else if (mat.rows() == 2)
        return mat(0, 0) * mat(1, 1) - mat(0, 1) * mat(1, 0);
    else if (mat.rows() == 3)
        return mat(0, 0) * (mat(1, 1) * mat(2, 2) - mat(1, 2) * mat(2, 1)) - mat(0, 1) * (mat(1, 0) * mat(2, 2) - mat(1, 2) * mat(2, 0)) + mat(0, 2) * (mat(1, 0) * mat(2, 1) - mat(1, 1) * mat(2, 0));

    assert(false);
    return T(0);
}