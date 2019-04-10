#include <stdio.h>
#include <opencv2/opencv.hpp>
#include "alg_conv.h"

using namespace cv;
#define ALG_CONV
int main(int argc, char** argv )
{

    if ( argc != 2 )
    {
        printf("usage: DisplayImage.out <Image_Path>\n");
        return -1;
    }

    Mat image;
    image = imread( argv[1], 1 );

    if ( !image.data )
    {
        printf("No image data \n");
        return -1;
    }
    //namedWindow("Display Image", WINDOW_AUTOSIZE );
    //imshow("Display Image", image);

    #ifdef ALG_CONV
    alg_conv(image);
    #endif
    return 0;
}
