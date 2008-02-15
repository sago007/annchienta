/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "mask.h"

#include <stdlib.h>
#include <png.h>
#include "auxfunc.h"

#define PNG_BYTES_TO_CHECK 4

namespace Annchienta
{

    Mask::Mask( const char *filename ): pixels(0)
    {
        png_byte buffer[PNG_BYTES_TO_CHECK];

        FILE *fp = fopen(filename, "rb");

        if( fp==NULL )
        {
            printf( "Error - could not open %s for reading.\n", filename );
            return;
        }

        /* Read in some of the signature bytes
         */
        if( fread( buffer, 1, PNG_BYTES_TO_CHECK, fp ) != PNG_BYTES_TO_CHECK )
        {
            printf( "Error - could not check png signature in %s.\n", filename );
            return;
        }

        /* Compare the first PNG_BYTES_TO_CHECK bytes of the signature.
         * Return nonzero (true) if they match
         */
        if( png_sig_cmp( buffer, (png_size_t)0, PNG_BYTES_TO_CHECK ) )
        {
            printf( "Error - png signature is not correct in %s.\n", filename );
            return;
        }

        /* variables for the png file handling */
        png_structp png_ptr;
        png_infop info_ptr;
        png_uint_32 png_width, png_height;
        int bit_depth, color_type, interlace_type;

        /* Note that we pass NULL to use the default error handling functions */
        png_ptr = png_create_read_struct( PNG_LIBPNG_VER_STRING, NULL, NULL, NULL );

        if( png_ptr==NULL )
        {
            fclose(fp);
            printf( "Error - failed creating png_ptr for %s.\n", filename );
            return;
        }

        /* Create our main structure */
        info_ptr = png_create_info_struct(png_ptr);

        /* In case something went wrong */
        if( info_ptr == NULL )
        {
            png_destroy_read_struct( &png_ptr, (png_infop*) NULL, (png_infop*) NULL);
            fclose(fp);
            printf( "Error - failed creating info_ptr for %s.\n", filename );
            return;
        }

        /* set up error handling */
        if( setjmp( png_jmpbuf( png_ptr ) ) )
        {
            /* Something went wrong */
            png_destroy_read_struct( &png_ptr, &info_ptr, (png_infop*) NULL);
            fclose(fp);
            printf( "Error - failed creating error handling for %s.\n", filename );
            return;
        }

        /* initialize the reading with regular C io functions */
        png_init_io( png_ptr, fp );
        /* then skip the bytes we have already read */
        png_set_sig_bytes( png_ptr, PNG_BYTES_TO_CHECK );

        /* Use the Hi-level method to read in the whole image
        * Note that we try not to use any transformations
        */
        png_read_png( png_ptr, info_ptr, PNG_TRANSFORM_IDENTITY, NULL );

        /* HERE WE SHOULD DO STUFF WITH IT */
        png_get_IHDR( png_ptr, info_ptr, &png_width, &png_height, &bit_depth, &color_type, &interlace_type, NULL, NULL );

        width = png_width;
        height = png_height;

        /* The pixel size: 1, 2, 3 or 4 usually */
        int pixelSize = png_get_rowbytes( png_ptr, info_ptr ) / png_width;
        /* allocate memory for the pixel data */
        pixels = (bool*) malloc( width * height );
        /* pointers to rows */
        png_byte **row_pointers = png_get_rows(png_ptr, info_ptr);
        
        /* set all pixels to their right values */
        for( unsigned int y=0; y<png_height; y++ )
        {
            for( unsigned int x=0; x<png_width; x++ )
            {
                png_byte *row = row_pointers[y];
                pixels[y*width+x] = row[ x*pixelSize ];
            }
        }

        /* clean up */
        png_destroy_read_struct( &png_ptr, &info_ptr, (png_infop*) NULL );

        /* close the file */
        fclose(fp);
    }

    Mask::~Mask()
    {
        delete[] pixels;
    }

    int Mask::getWidth() const
    {
        return width;
    }

    int Mask::getHeight() const
    {
        return height;
    }

    bool Mask::collision( int x1, int y1, Mask *mask2, int x2, int y2, bool box )
    {
        int left1, left2, over_left;
        int right1, right2, over_right;
        int top1, top2, over_top;
        int bottom1, bottom2, over_bottom;
        int over_width, over_height;

        left1 = x1;
        left2 = x2;
        right1 = x1 + width;
        right2 = x2 + mask2->width;
        top1 = y1;
        top2 = y2;
        bottom1 = y1 + height;
        bottom2 = y2 + mask2->height;


        /* First, do some trivial rejections:
         */
        if( bottom1 < top2 )
            return false;
        if( top1 > bottom2 )
            return false;
        if( right1 < left2 )
            return false;
        if( left1 > right2 )
            return false;

        if( box )
            return true;

        /* Ok, compute the rectangle which intersects:
         */
        over_bottom = min( bottom1, bottom2 );
        over_top = max( top1, top2 );
        over_right = min( right1, right2 );
        over_left = max( left1, left2 );

        over_width = over_right - over_left;
        over_height = over_bottom - over_top;

        int mx1 = over_left - left1;
        int my1 = over_top - top1;

        int mx2 = over_left - left2;
        int my2 = over_top - top2;

        for( int y=0; y<over_height; y++ )
        {
            for( int x=0; x<over_width; x++ )
            {
                if( pixels[my1*width+mx1] && mask2->pixels[my2*mask2->width+mx2] )
                    return true;
                mx1++;
                mx2++;
            }
            my1++;
            my2++;
            mx1 = over_left - left1;
            mx2 = over_left - left2;
        }

        return false;
    }

};
