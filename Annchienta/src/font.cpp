/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "font.h"

#include <ft2build.h>
#include FT_FREETYPE_H

#include "auxfunc.h"

#define NUM_CHARACTERS 128

namespace Annchienta
{
    Font::Font( const char *filename, int size )
    {
        /* Create the main library and init it.
         */
        FT_Library library;
        if( FT_Init_FreeType( &library ) )
        {
            printf( "Error - could not create main FreeType library." );
            return;
        }
    
        /* Load the actual font.
         */
        FT_Face face;
        if( FT_New_Face( library, filename, 0, &face ) )
        {
            printf( "Error - could not open %s as TTF font.", filename );
            return;
        }

        /* Set some members.
         */
        textures = new GLuint[NUM_CHARACTERS];
        height = size;
        lineHeight = (int)(1.6f*(float)size);
        advance = new int[NUM_CHARACTERS];

        /* Allocate memory for our font structure.
         */
        list = glGenLists(NUM_CHARACTERS);
        glGenTextures( NUM_CHARACTERS, textures );

        /* Set the pixel size.
         */
        FT_Set_Pixel_Sizes( face, 0, (FT_UInt) height );
    
        /* Create a list for every character.
         */
        for( unsigned int i=0; i<NUM_CHARACTERS; i++ )
        {
            FT_UInt index = FT_Get_Char_Index( face, i );
            if( FT_Load_Glyph( face, index, FT_LOAD_RENDER ) )
            {
                printf( "Ft_Load_Glyph for %c int %s returned error code.", (char)i, filename );
                return;
            }
    
            FT_GlyphSlot glyph = face->glyph;
            FT_Bitmap &bitmap = glyph->bitmap;

            int width = bitmap.width;
            int height = bitmap.rows;
            int glWidth = nearestPowerOfTwo( width );
            int glHeight = nearestPowerOfTwo( height );

            float rightTexCoord = ((float)width)/((float)glWidth);
            float bottomTexCoord = ((float)height)/((float)glHeight);

            advance[i] = glyph->advance.x >> 6;
            int left = glyph->metrics.horiBearingX >> 6;
            int move_down = ( glyph->metrics.height - glyph->metrics.horiBearingY ) >> 6;

            /* Allocate room for some pixels.
             */
            GLubyte pixels[ glWidth * glHeight * 2 ];
        
            /* Set the pixels to their right values.
             */
            for( unsigned int y=0; y<height; y++ )
            {
                for( unsigned int x=0; x<width; x++ )
                {
                    pixels[ ((x+glWidth*y)<<1) ] = 255;
                    pixels[ ((x+glWidth*y)<<1) + 1 ] = bitmap.buffer[ x+width*y ];
                }
            }

            /* Select the right texture and set some parameters.
             */
            glBindTexture( GL_TEXTURE_2D, textures[i] );
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);

            /* Create our texture.
             */
            glTexImage2D( GL_TEXTURE_2D, 0, GL_LUMINANCE_ALPHA, glWidth, glHeight, 0, GL_LUMINANCE_ALPHA, GL_UNSIGNED_BYTE, pixels );

            /* Start our display list.
             */
            glNewList( list+i, GL_COMPILE );

            /* Alright. First, we move a little, so the character has
             * some space to it's left.
             */
            glTranslatef( left, 0.0f, 0.0f );

            /* Now draw a quad.
             */
            glBindTexture( GL_TEXTURE_2D, textures[i] );
            glBegin( GL_QUADS );

                glTexCoord2f( 0.0f, bottomTexCoord );
                //glVertex2f( 0.0f, 0.0f );
                glVertex2f( 0.0f, move_down );

                glTexCoord2f( rightTexCoord, bottomTexCoord );
                //glVertex2f( 10.0f, 0.0f );
                glVertex2f( width, move_down );

                glTexCoord2f( rightTexCoord, 0.0f );
                //glVertex2f( 10.0f, 10.0f );
                glVertex2f( width, -height+move_down );

                glTexCoord2f( 0.0f, 0.0f );
                //glVertex2f( 0.0f, 10.0f );
                glVertex2f( 0.0f, -height+move_down );

            glEnd();

            /* Again, move to the right to make space for the
             * next character.
             */
            glTranslatef( advance[i]-left, 0.0f, 0.0f );

            /* Finish up our display list.
             */
            glEndList();
        }
    
        /* Free up our resources.
         */
        FT_Done_Face( face );
        FT_Done_FreeType( library );
    }

    Font::~Font()
    {
        glDeleteLists( list, NUM_CHARACTERS );
        glDeleteTextures( NUM_CHARACTERS, textures );
        delete[] textures;
        delete[] advance;
    }

    int Font::getHeight() const
    {
        return height;
    }

    int Font::getLineHeight() const
    {
        return lineHeight;
    }

    int Font::getStringWidth( const char *text ) const
    {
        int width = 0;
        while( *text )
        {
            width += advance[*text];
            text++;
        }
        return width;
    }

    void Font::draw( const char *text, int x, int y ) const
    {
        glPushMatrix();

        glTranslatef( x, y+height, 0.0f );

        glListBase( list );
        glCallLists( strlen(text), GL_UNSIGNED_BYTE, text );

        glPopMatrix();
    }

};
