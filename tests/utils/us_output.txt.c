void compute(double values[], int num_points, double ders[]){

	for(int i = 0; i < num_points; ++i)
	{
		double c = values[i* 1 + 0 ];
		ders[i*1+0]= 1.; // df/(c) 
	}
}

