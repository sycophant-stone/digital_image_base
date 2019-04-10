#include <stdio.h>
#include <opencv2/opencv.hpp>
#include "alg_conv.h"
using namespace cv;
Mat _conv(Mat img, Mat kernel)
{
    char *src=img.data;
    char *dst=kernel.data;
    for(int i=0;i<img.rows;i++){
        for(int j=0;j<img.cols;j++){
            int temp= 0;
            for(int ki=0;ki<kernel.rows;ki++){
                for(int kj=0;kj<kernel.cols;kj++){
                    temp+=src[i*img.rows+j]*kernel[ki*kernel.rows+kj]
                }
            }
        }
    }
}
Mat alg_conv(Mat img)
{
    Mat kernel(3,3,CV_8UC3,3);// r,c, type, chn
    Mat dst;
    int kr,kc;
    kr = kernel.rows;
    kc = kernel.cols;
    char * src = kernel.data;
    for(int i=0;i<kr;i++){
        for(int j=0;j<kc;j++){
            src[i*3+j] = 1;
        }
    }
    dst = _conv(img,kernel);
    return dst;
}