Command Line Scripts
====================

ortho
-----

``ortho`` – Query fonts about orthographic support.

Usage
~~~~~

``ortho [-h] [-f] [-p] [-n NEAR_MISS] font [font ...]``

When called without any options, `ortho` will determine the orthographic support of the supplied font(s) by looking at the required characters for each orthography.

.. code-block:: bash
   
   $ ortho ComicJens.ttf 
   The font supports 104 orthographies:
   Afrikaans
   Albanian
   Asu (Tanzania)
   Azeri
   Basque
   Bemba
   Bena
   Bosnian
   Catalan
   [...]
   Zulu

Options
~~~~~~~

``-f | --full-only``

   The `-f` option only lists orthographies for which all required *and* optional characters are present in the font.

   .. code-block:: bash
   
      $ ortho -f ComicJens.ttf
      The font supports 98 orthographies:
      Afrikaans
      Albanian
      Asu (Tanzania)
      Azeri
      Basque
      Bemba
      Bena
      Bosnian
      Catalan
      [...]
      Zulu

``-p | --punctuation``

   Prints a list of orthographies for which all letter category characters are present in the font, but have missing punctuation category characters. For the missing characters, Unicode, glyph name, and Unicode name are reported.
   
   .. code-block:: bash
   
      $ ortho -p ComicJens.ttf
      Orthographies which can be supported by adding punctuation characters:
      
      Scottish Gaelic
          0x204A	uni204A	Tironian Sign Et

``-n N | --near-miss N``

   Prints a list of orthographies which are lacking up to a number of N characters to be supported.    For the missing characters, Unicode, glyph name, and Unicode name are reported.
   
   .. code-block:: bash
      
      $ ortho -n 1 ComicJens.ttf
      Orthographies which can be supported with max. 1 additional character:
      
      Breton
          0x02BC	uni02BC	Modifier Letter Apostrophe
      
      Hawaiian
          0x02BB	uni02BB	Modifier Letter Turned Comma
      
      Quechua
          0x02BC	uni02BC	Modifier Letter Apostrophe
      
      Tongan
          0x02BB	uni02BB	Modifier Letter Turned Comma
