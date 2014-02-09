/*   TESTING THE SIMPLE AUDIO I/O LIB
	 Frank Zalkow, 2014
	 
	 compile with:
	 gcc -o test main.c -lsndfile -lportaudio -include audioio.c
*/

#include "audioio.h"
	 
// MAIN FUNCTION
int main () {
	//play_from_file("test1.wav");
	record_to_file("test2.wav", 1, 1);
	return 0;
}
