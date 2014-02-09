/*   SIMPLE AUDIO I/O LIB
     depends on libsndfile: http://www.mega-nerd.com/libsndfile
     and portaudio:         http://www.portaudio.com/	 
     Frank Zalkow, 2014
*/

// play an audio file
static void play_from_file (const char *infilename);

// record an audio file
static void record_to_file (const char *outfilename, unsigned int duration, short channels);
