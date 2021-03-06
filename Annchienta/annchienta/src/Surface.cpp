/*  This file is part of Annchienta.
 *  Copyright 2008 (C) Jasper Van der Jeugt
 *
 *  Annchienta is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Annchienta is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 * 
 *  You should have received a copy of the GNU General Public License
 *  along with Annchienta.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "Surface.h"

#include <cstdlib>
#include <png.h>

#include "LogManager.h"
#include "MathManager.h"
#include "VideoManager.h"

#define PNG_BYTES_TO_CHECK 4

namespace Annchienta
{

    void Surface::generateTextureFromPixels()
    {
        /* Find out texture coords. */
        leftTexCoord = 0.0f;
        topTexCoord = 1.0f;
        rightTexCoord = (float)(width)/(float)(glWidth);
        bottomTexCoord = 1.0f - (float)(height)/(float)(glHeight);

        /* If there already is a texture, delete it. */
        if( glIsTexture( texture ) == GL_TRUE )
            glDeleteTextures( 1, &texture );

        /* Generate our texture and bind it. */
        glGenTextures( 1, &texture );
        glBindTexture( GL_TEXTURE_2D, texture );

        /* Set parameters.
         *
         * It is quite important to note that we choose to use GL_NEAREST. Where,
         * in regular OpenGL applications, you would probably want to use GL_LINEAR
         * for better quality. But the reason we choose for GL_NEAREST is because
         * or drawings will be more "pixel perfect" this way... */
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);

        /* Choose a fitting format. */
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

        /* Write our pixel data to the video memory. */
        glTexImage2D( GL_TEXTURE_2D, 0, pixelSize, glWidth, glHeight, 0, format, GL_UNSIGNED_BYTE, (GLvoid*) pixels );

        /* Clean up the pixel data. */
        delete[] pixels;
        pixels = 0;
    }

    void Surface::compileList()
    {
        /* If there is no list already, generate one. */
        if( glIsList( list ) == GL_FALSE )
            list = glGenLists( 1 );

        glNewList( list, GL_COMPILE );

        glBindTexture( GL_TEXTURE_2D, texture );
        glBegin( GL_QUADS );
            glTexCoord2f( leftTexCoord, topTexCoord );
            glVertex2f( 0.0f, 0.0f );
            glTexCoord2f( leftTexCoord, bottomTexCoord );
            glVertex2f( 0.0f, (GLfloat)height );
            glTexCoord2f( rightTexCoord, bottomTexCoord );
            glVertex2f( (GLfloat)width, (GLfloat)height );
            glTexCoord2f( rightTexCoord, topTexCoord );
            glVertex2f( (GLfloat)width, 0.0f );
        glEnd();

        glEndList();
    }

    Surface::Surface( int w, int h, int ps ): Cacheable(0), width(w), height(h), pixelSize(ps), texture(0), list(0)
    {
        VideoManager *videoManager = getVideoManager();
        LogManager *logManager = getLogManager();
        if( !videoManager->isVideoModeSet() )
            logManager->error( "Attempting to create a Surface before the video mode was set." );

        /* Calculate the actual memory size. */
        MathManager *mathManager = getMathManager();
        glWidth = mathManager->nearestPowerOfTwo( width );
        glHeight = mathManager->nearestPowerOfTwo( height );

        pixels = new GLubyte[ glWidth * glHeight * pixelSize ];

        generateTextureFromPixels();
        compileList();
    }

    Surface::Surface( const char *filename ): Cacheable(filename), texture(0), list(0)
    {
        /* We might need some logging and some math here. */
        MathManager *mathManager = getMathManager();
        VideoManager *videoManager = getVideoManager();
        LogManager *logManager = getLogManager();
        if( !videoManager->isVideoModeSet() )
            logManager->error( "Attempting to create a Surface before the video mode was set." );

        png_byte buffer[PNG_BYTES_TO_CHECK];
        
        FILE *fp = fopen(filename, "rb");
    
        if( fp==NULL )
            logManager->error( "Could not open '%s' for reading.", filename );
        
        /* Read in some of the signature bytes */
        if( fread( buffer, 1, PNG_BYTES_TO_CHECK, fp ) != PNG_BYTES_TO_CHECK )
            logManager->error( "Could not check png signature in '%s'.", filename );
        
        /* Compare the first PNG_BYTES_TO_CHECK bytes of the signature.
         * Return nonzero (true) if they match */
        if( png_sig_cmp( buffer, (png_size_t)0, PNG_BYTES_TO_CHECK ) )
            logManager->error( "PNG signature is not correct in '%s'.", filename );
    
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
            logManager->error( "Failed creating png_ptr for '%s'.", filename );
        }
    
        /* Create our main structure */
        info_ptr = png_create_info_struct(png_ptr);
    
        /* In case something went wrong */
        if( info_ptr == NULL )
        {
            png_destroy_read_struct( &png_ptr, (png_infop*) NULL, (png_infop*) NULL);
            fclose(fp);
            logManager->error( "Failed creating info_ptr for '%s'.", filename );
        }
    
        /* set up error handling */
        if( setjmp( png_jmpbuf( png_ptr ) ) )
        {
            /* Something went wrong */
            png_destroy_read_struct( &png_ptr, &info_ptr, (png_infop*) NULL);
            fclose(fp);
            logManager->error( "Failed creating error handling for '%s'.", filename );
            return;
        }
    
        /* initialize the reading with regular C io functions */
        png_init_io( png_ptr, fp );
        /* then skip the bytes we have already read */
        png_set_sig_bytes( png_ptr, PNG_BYTES_TO_CHECK );
    
        /* Use the Hi-level method to read in the whole image
        *  Note that we try not to use any transformation */
        png_read_png( png_ptr, info_ptr, PNG_TRANSFORM_IDENTITY, NULL );
    
        /* Get info about the whole image. */
        png_get_IHDR( png_ptr, info_ptr, &png_width, &png_height, &bit_depth, &color_type, &interlace_type, NULL, NULL );

        width = png_width;
        height = png_height;
        glWidth = mathManager->nearestPowerOfTwo( png_width ),
        glHeight = mathManager->nearestPowerOfTwo( png_height );

        /* The pixel size: 1, 2, 3 or 4 usually */
        pixelSize = png_get_rowbytes( png_ptr, info_ptr ) / png_width;

        /* allocate memory for the pixel data */
        pixels = new GLubyte[ pixelSize * glWidth * glHeight ];

        /* pointers to rows */
        png_byte **row_pointers = png_get_rows(png_ptr, info_ptr);

        /* set all pixels to their right values */
        for( unsigned int y=0; y<png_height; y++ )
        {
            for( unsigned int x=0; x<png_width; x++ )
            {
                /* Get the correct row. */
                png_byte *row = row_pointers[y];

                /* The first byte offset */
                unsigned int firstByte = x * pixelSize;

                /* Kind of 'mirror' around the x-axis now. */
                int my = glHeight - y - 1;

                /* Set all the bytes. */
                for( int b=0; b<pixelSize; b++ )
                    pixels[ glWidth*pixelSize*my + x*pixelSize + b ] = row[ firstByte + b ];
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

    CacheableType Surface::getCacheableType() const
    {
        return SurfaceCacheable;
    }

    int Surface::getWidth() const
    {
        return width;
    }

    int Surface::getHeight() const
    {
        return height;
    }

    void Surface::setLinearScaling() const
    {
        glBindTexture( GL_TEXTURE_2D, texture );
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    }

    void Surface::setNearestScaling() const
    {
        glBindTexture( GL_TEXTURE_2D, texture );
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
    }

    void Surface::draw( int x, int y ) const
    {
        glPushMatrix();

        glTranslatef( (GLfloat)x, (GLfloat)y, 0.0f );
        glCallList( list );

        glPopMatrix();
    }

    void Surface::draw( int dx, int dy, int sx1, int sy1, int sx2, int sy2 ) const
    {
        float left = (float)sx1/(float)getGlWidth(),
              right = (float)sx2/(float)getGlWidth(),
              top = 1.0f - (float)sy1/(float)getGlHeight(),
              bottom = 1.0f - (float)sy2/(float)getGlHeight();

        glBindTexture( GL_TEXTURE_2D, getTexture() );
        glBegin( GL_QUADS );

            glTexCoord2f( left, top );
            glVertex2f( (GLfloat)dx, (GLfloat)dy );

            glTexCoord2f( left, bottom );
            glVertex2f( (GLfloat)dx, (GLfloat)(dy+sy2-sy1) );

            glTexCoord2f( right, bottom );
            glVertex2f( (GLfloat)(dx+sx2-sx1), (GLfloat)(dy+sy2-sy1) );

            glTexCoord2f( right, top );
            glVertex2f( (GLfloat)(dx+sx2-sx1), (GLfloat)dy );
        glEnd();
    }

    void Surface::draw( int x1, int y1, int x2, int y2 ) const
    {
        glBindTexture( GL_TEXTURE_2D, getTexture() );
        glBegin( GL_QUADS );

            glTexCoord2f( getLeftTexCoord(), getTopTexCoord() );
            glVertex2f( (GLfloat)x1, (GLfloat)y1 );

            glTexCoord2f( getLeftTexCoord(), getBottomTexCoord() );
            glVertex2f( (GLfloat)x1, (GLfloat)y2 );

            glTexCoord2f( getRightTexCoord(), getBottomTexCoord() );
            glVertex2f( (GLfloat)x2, (GLfloat)y2 );

            glTexCoord2f( getRightTexCoord(), getTopTexCoord() );
            glVertex2f( (GLfloat)x2, (GLfloat)y1 );
        glEnd();
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
