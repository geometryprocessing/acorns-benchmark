// #include <math.h>

// int main(int argc, char const *argv[])
// {
//     return 0;
// }

/*
local_disp: n_local_disp x size (3)
grads: n_pts x n_grads x size (3)
vjac_it: n_pts x size x size (3)
da: n_pts x 1
*/

double func(const double *local_disp, const int n_local_disp, const double *grads, const int n_grads, const double *vjac_it, const double *da, const int n_pts, const double mu, const double lambda)
{
    const int size = 3; // hardcoded
    int n_grads = 4;   //grads_size / da_size / size; = 36 / 6 / 2 ; 132 /  11 / 3 = 4
    // double mu = 0.384615;
    // double lambda = 0.32967;
    // run multiple times with p = 0,1,1..6.
    // only initialize constants

    // for (long p = 0; p < n_pts; ++p)
    // {
    for (long k1 = 0; k1 < size; ++k1)
    {
        for (long k2 = 0; k2 < size; ++k2)
            def_grad[k1][k2] = 0.;
    }

    for (int i = 0; i < n_grads; ++i)
    {
        for (int d = 0; d < size; ++d)
        {
            for (int c = 0; c < size; ++c)
            {
                def_grad[d][c] = def_grad[d][c] + grads[(i + p * n_grads) * size + c] * local_disp[i * size + d];
            }
        }
    }

    //     double jac_it[3][3];

    for (long k1 = 0; k1 < size; ++k1)
    {
        for (long k2 = 0; k2 < size; ++k2)
        {
            jac_it[k1][k2] = vjac_it[p * size * size + k2 * size + k1];
        }
    }

    for (int c = 0; c < size; c++)
    {
        for (int d = 0; d < size; d++)
        {
            mult[c][d] = def_grad[c][0] * jac_it[0][d] + def_grad[c][1] * jac_it[1][d] + def_grad[c][2] * jac_it[2][d];
        }
    }

    //     //Id + grad d
    for (int d = 0; d < size; ++d)
        mult[d][d] = mult[d][d] + 1;

    const double det_def_grad = mult[0][0] * (mult[1][1] * mult[2][2] - mult[1][2] * mult[2][1]) - mult[0][1] * (mult[1][0] * mult[2][2] - mult[1][2] * mult[2][0]) + mult[0][2] * (mult[1][0] * mult[2][1] - mult[1][1] * mult[2][0]);

    for (int c = 0; c < size; c++)
    {
        for (int d = 0; d < size; d++)
        {
            mult1[c][d] = mult[c][0] * mult[d][0] + mult[c][1] * mult[d][1] + mult[c][2] * mult[d][2];
        }
    }

    trace = mult1[0][0] + mult1[1][1] + mult1[2][2];

    // for(int k = 0; k < size; ++k)
    //     trace = trace + mult1[k][k];

    const double log_det_j = log(det_def_grad);
    const double val = mu / 2. * (trace - size - 2 * log_det_j) + lambda / 2 * log_det_j * log_det_j;

    // for p=6
    energy = energy + val * da[p];
    // // }

    // return energy;
}
