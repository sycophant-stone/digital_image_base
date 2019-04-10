#include <stdio.h>
#include<iostream>
#include <opencv2/opencv.hpp>
#include "include\alg_conv.h"

using namespace std;
using namespace cv;

#define GET_DATA(m,r,c) *( (int*)(m.data+r*m.step[0]+m.step[1]*c))

Mat _conv(Mat img, Mat kernel)
{
	Mat dst = Mat(img.cols, img.rows, img.type(),img.channels());
	int r = kernel.cols / 2;

    for(int i=0;i<img.cols;i++){
        for(int j=0;j<img.rows;j++){
            int temp= 0;
            for(int ki=0;ki<kernel.cols;ki++){
                for(int kj=0;kj<kernel.rows;kj++){
					temp += GET_DATA(img, j, i)*GET_DATA(kernel, kj, ki);
                }
            }
			if (i + r*img.cols + r + j < img.rows*img.cols) {
				GET_DATA(dst, j + r, i + r) = temp;
			}
        }
    }
	return dst;
}
Mat alg_conv(Mat img)
{
    Mat kernel(3,3,img.type(),img.channels());// r,c, type, chn
    Mat dst;
	int kr, kc, sum = 0;
    kr = kernel.rows;
    kc = kernel.cols;
    for(int i=0;i<kr;i++){
        for(int j=0;j<kc;j++){
			GET_DATA(kernel, i,j) = 1;
			sum += GET_DATA(kernel, i, j);
        }
    }
	// normalize
	for (int i = 0; i<kr; i++) {
		for (int j = 0; j<kc; j++) {
			GET_DATA(kernel, i, j) /= sum;
		}
	}

    dst = _conv(img,kernel);
	//filter2D(img, dst, img.depth(), kernel, Point(1, 1), 0.0, BORDER_CONSTANT); // exception occurs
    return dst;
}