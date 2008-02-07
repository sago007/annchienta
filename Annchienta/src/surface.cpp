/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "surface.h"

#include <stdlib.h>
#include <png.h>

#include "auxfunc.h"

#define PNG_BYTES_TO_CHECK 4

namespace Annchienta
{

    void Surface::generateTextureFromPixels()
    {
        /* Find out texture coords.
         */
        leftTexCoord = 0.0f;
        topTexCoord = 1.0f;
        rightTexCoord = (float)(width)/(float)(glWidth);
        bottomTexCoord = 1.0 - (float)(height)/(float)(glHeight);

        /* If there already is a texture, delete it.
         */
        if( glIsTexture( texture ) == GL_TRUE )
            glDeleteTextures( 1, &texture );

        /* Generate our texture and bind it.
         */
        glGenTextures( 1, &texture );
        glBindTexture( GL_TEXTURE_2D, texture );

        /* Set parameters.
         *
         * It is quite important to note that we choose to use GL_NEAREST. Where,
         * in regular OpenGL applications, you would probably want to use GL_LINEAR
         * for better quality. But the reason we choose for GL_NEAREST is because
         * or drawings will be more "pixel perfect" this way...
         */
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);

        /* Choose a fitting format.
         */
        GLenum format;
        switch( pixelSize )
        {
            case 1:
                format = GL_LUMINANCE;
                break;
            case 2:
                format = GL_LUMINANCE_ALPHA;
                break;
            case 3:
                format = GL_RGB;
                break;
            case 4: default:
                format = GL_RGBA;
                break;
        }

        /* Write our pixel data to the video memory.
         */
        glTexImage2D( GL_TEXTURE_2D, 0, pixelSize, glWidth, glHeight, 0, format, GL_UNSIGNED_BYTE, (GLvoid*) pixels );

        /* Clean up the pixel data.
         */
        delete[] pixels;
        pixels = 0;
    }

    void Surface::compileList()
    {
        /* If there is no list already, generate one.
         */
        if( glIsList( list ) == GL_FALSE )
            list = glGenLists( 1 );

        glNewList( list, GL_COMPILE );

        glBindTexture( GL_TEXTURE_2D, texture );
        glBegin( GL_QUADS );
            glTexCoord2f( leftTexCoord, topTexCoord );
            glVertex2f( 0, 0 );
            glTexCoord2f( leftTexCoord, bottomTexCoord );
            glVertex2f( 0, height );
            glTexCoord2f( rightTexCoord, bottomTexCoord );
            glVertex2f( width, height );
            glTexCoord2f( rightTexCoord, topTexCoord );
            glVertex2f( width, 0 );
        glEnd();

        glEndList();
    }

    Surface::Surface( int w, int h, int ps ): width(w), height(h), pixelSize(ps), texture(0), list(0)
    {
        glWidth = nearestPowerOfTwo( width );
        glHeight = nearestPowerOfTwo( height );

        pixels = new GLubyte[ glWidth * glHeight * pixelSize ];

        generateTextureFromPixels();
        compileList();
    }

    Surface::Surface( const char *filename ): texture(0), list(0)
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
        glWidth = nearestPowerOfTwo( png_width ),
        glHeight = nearestPowerOfTwo( png_height );

        /* The pixel size: 1, 2, 3 or 4 usually */
        pixelSize = png_get_rowbytes( png_ptr, info_ptr ) / png_width;
        /* allocate memory for the pixel data */
        pixels = (GLubyte*) malloc( pixelSize * glWidth * glHeight );
        /* pointers to rows */
        png_byte **row_pointers = png_get_rows(png_ptr, info_ptr);
        
        /* set all pixels to their right values */
        for( unsigned int y=0; y<png_height; y++ )
        {
            for( unsigned int x=0; x<png_width; x++ )
            {
                png_byte *row = row_pointers[y];
                unsigned int firstByte = x * pixelSize;
                int my = glHeight - y - 1;
                for( unsigned int b=0; b<pixelSize; b++ )
                {
                    pixels[ glWidth*pixelSize*my + x*pixelSize + b ] = row[ firstByte + b ];
                }
            }
        }
    
        /* clean up */
        png_destroy_read_struct( &png_ptr, &info_ptr, (png_infop*) NULL );
    
        /* close the file */
        fclose(fp);

        generateTextureFromPixels();
        compileList();
    }

    Surface::~Surface()
    {
        glDeleteTextures( 1, &texture );
        glDeleteLists( list, 1 );
        if( pixels )
            delete[] pixels;
    }

    int Surface::getWidth() const
    {
        return width;
    }

    int Surface::getHeight() const
    {
        return height;
    }

    void Surface::draw( int x, int y ) const
    {
        glPushMatrix();

        glTranslatef( x, y, 0.0f );
        glCallList( list );

        glPopMatrix();
    }

    GLuint Surface::getTexture() const
    {
        return texture;
    }

    int Surface::getGlWidth() const
    {
        return glWidth;
    }

    int Surface::getGlHeight() const
    {
        return glHeight;
    }

    float Surface::getLeftTexCoord() const
    {
        return leftTexCoord;
    }

    float Surface::getRightTexCoord() const
    {
        return rightTexCoord;
    }

    float Surface::getTopTexCoord() const
    {
        return topTexCoord;
    }

    float Surface::getBottomTexCoord() const
    {
        return bottomTexCoord;
    }

};
