/*   SIMPLE AUDIO I/O LIB
     depends on libsndfile: http://www.mega-nerd.com/libsndfile
     and portaudio:         http://www.portaudio.com/	 
     Frank Zalkow, 2014
*/

#include "sfconfig.h"
#include <stdio.h>
#include <stdlib.h>
#include <sndfile.h>
#include <string.h>
#include "portaudio.h"

#define	BUFFER_LEN 4096


/* +++ play a given audio file +++
   - at the moment restricted to 16 bit audio files
   - channels of output are same as channels of audiofile, so if you have only
     stereo output, you can only play back mono or stereo files
   - only tested with WAVE files */
static void play_from_file (const char *infilename) {
	SNDFILE *infile;
	SF_INFO sfinfo;
	sf_count_t readcount ;
	
	PaError err;
	PaStreamParameters outputParameters;
	PaStream *stream;

	int i;
	
	// --- 1. open the audiofile ---
	if (! (infile = sf_open (infilename, SFM_READ, &sfinfo))) {
		printf ("Error : could not open file : %s\n", infilename) ;
		puts (sf_strerror (NULL)) ;
		exit (EXIT_FAILURE) ;
	}
	printf("%s is a file with %i channel(s) and with a samplerate of %i.\n", infilename, sfinfo.channels, sfinfo.samplerate);

	// --- 2. initialize portaudio for playback ---
	err = Pa_Initialize();
	if( err != paNoError ) {
		printf("Error : could not initialize Portaudio.\n");
		exit (EXIT_FAILURE) ;
	}

	outputParameters.device = Pa_GetDefaultOutputDevice();
	outputParameters.channelCount = sfinfo.channels;
	outputParameters.sampleFormat = paInt16; // at the moment only 16 bit files
	outputParameters.suggestedLatency = Pa_GetDeviceInfo( outputParameters.device )->defaultHighOutputLatency;
	outputParameters.hostApiSpecificStreamInfo = NULL;

	err = Pa_OpenStream(
		&stream,
		NULL,
		&outputParameters,
	    sfinfo.samplerate,
	    BUFFER_LEN,
		paClipOff,      /* we won't output out of range samples so don't bother clipping them */
		NULL, /* no callback, use blocking API */
		NULL ); /* no callback, so no callback userData */
	if( err != paNoError ) {
		printf("Error : could not initialize Portaudio.\n");
		exit (EXIT_FAILURE) ;
	}

	err = Pa_StartStream( stream );
	if( err != paNoError ) {
		printf("Error : could not initialize Portaudio.\n");
		exit (EXIT_FAILURE) ;
	}

	// --- 3. read file and play each chunk ---
	int buffer_len_multichannel = BUFFER_LEN * sfinfo.channels;
	short *buffer = malloc(buffer_len_multichannel * sizeof(short));
	if (buffer == NULL) {
		printf("Not enough memory. Could not malloc a buffer of %i short-integers.\n", buffer_len_multichannel);
		exit(EXIT_FAILURE);
	}
	while ((readcount = sf_read_short (infile, buffer, buffer_len_multichannel)) > 0) {
		err = Pa_WriteStream( stream, buffer, BUFFER_LEN);
		if( err != paNoError ) {
			printf("Error while playback.\n");
			free(buffer);
			Pa_StopStream( stream );
			Pa_CloseStream( stream );
			Pa_Terminate();
			sf_close(infile);
			exit (EXIT_FAILURE) ;
		}
	}
	free(buffer);
	
	// --- 4. close the file and the portaudio connection ---
	Pa_StopStream( stream );
	Pa_CloseStream( stream );
	Pa_Terminate();
	sf_close(infile);

}

/* +++ record an audio file+++
   - only 16 bit audio files at the moment */
static void record_to_file (const char *outfilename, unsigned int duration, short channels) {
	int sample_rate = 44100;
	double sample_count = (1 + (sample_rate * duration)/BUFFER_LEN)*BUFFER_LEN;
	SNDFILE *outfile;
	SF_INFO	sfinfo ;
	int i;
	
	PaError err;
	PaStreamParameters inputParameters;
	PaStream *stream;

	// --- 1. open the audiofile ---
	memset (&sfinfo, 0, sizeof (sfinfo)) ; // why ???
	sfinfo.samplerate = sample_rate;
	sfinfo.frames = sample_count*channels;
	sfinfo.channels = channels;
	sfinfo.format = (SF_FORMAT_WAV | SF_FORMAT_PCM_16);

	if (! (outfile = sf_open (outfilename, SFM_WRITE, &sfinfo))) {
		printf ("Error : Not able to open output file.\n") ;
		exit (EXIT_FAILURE) ;
	} ;

	// --- 2. initialize portaudio for recording ---
	err = Pa_Initialize();
	if( err != paNoError ) {
		printf("Error : could not initialize Portaudio.\n");
		exit (EXIT_FAILURE) ;
	}

    inputParameters.device = Pa_GetDefaultInputDevice();
    inputParameters.channelCount = channels;
    inputParameters.sampleFormat = paInt16; // at the moment only 16 bit files
    inputParameters.suggestedLatency = Pa_GetDeviceInfo( inputParameters.device )->defaultHighOutputLatency;
    inputParameters.hostApiSpecificStreamInfo = NULL;

	err = Pa_OpenStream(
		&stream,
		&inputParameters,
		NULL,
	    sample_rate,
	    BUFFER_LEN,
		paClipOff,      /* we won't output out of range samples so don't bother clipping them */
		NULL, /* no callback, use blocking API */
		NULL ); /* no callback, so no callback userData */
	if( err != paNoError ) {
		printf("Error : could not initialize Portaudio.\n");
		exit (EXIT_FAILURE) ;
	}

	err = Pa_StartStream( stream );
	if( err != paNoError ) {
		printf("Error : could not initialize Portaudio.\n");
		exit (EXIT_FAILURE) ;
	}

	// --- 3. record audio and write to file ---
	int buffer_len_multichannel = BUFFER_LEN * channels;
	short *buffer = malloc(buffer_len_multichannel * sizeof(short));
	if (buffer == NULL) {
		printf("Not enough memory. Could not malloc a buffer of %i short-integers.\n", buffer_len_multichannel);
		exit(EXIT_FAILURE);
	}

	for(i = 0; i < sample_count/BUFFER_LEN; i++ ) {
		err = Pa_ReadStream(stream, buffer, BUFFER_LEN );

		printf("%d ", buffer[0]);
		
	    if( err != paNoError ) {
			printf("Error while recording.\n");
			free(buffer);
			Pa_StopStream( stream );
			Pa_CloseStream( stream );
			Pa_Terminate();
			sf_close(outfile);
			exit (EXIT_FAILURE) ;
		}

		if (sf_write_short (outfile, buffer, buffer_len_multichannel) != buffer_len_multichannel) {
			printf("Error while writing to file.\n");
			free(buffer);
			Pa_StopStream( stream );
			Pa_CloseStream( stream );
			Pa_Terminate();
			sf_close(outfile);
			exit (EXIT_FAILURE) ;
		}
	}

    free(buffer);
	Pa_StopStream( stream );
	Pa_CloseStream( stream );
	Pa_Terminate();
	sf_close(outfile);
}
