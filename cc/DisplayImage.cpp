#include <stdio.h>
#include <opencv2/opencv.hpp>
#include "alg_conv.h"

using namespace cv;
#define ALG_CONV
int main(int argc, char** argv )
{
#if 0
    if ( argc != 2 )
    {
        printf("usage: DisplayImage.out <Image_Path>\n");
        return -1;
    }
#endif
    Mat image;
	Mat img_post;
    image = imread("../../lena.jpg" , 1 );

    if ( !image.data )
    {
        printf("No image data \n");
        return -1;
    }
#if 0
    namedWindow("Display Image", WINDOW_AUTOSIZE );
    imshow("Display Image", image);
	waitKey();
#else 
    #ifdef  ALG_CONV
	img_post = alg_conv(image);
	namedWindow("Processed Img", WINDOW_AUTOSIZE);
	imshow("Processed Img", img_post);
	waitKey();
    #endif
#endif
    return 0;
}
