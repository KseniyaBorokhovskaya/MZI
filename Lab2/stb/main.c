#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>

#include "stb.h"

#define KEY_SIZE 32
#define BLOCK_SIZE 16
#define ENCRYPTION_MODE 1
#define DECRYPTION_MODE 0
#define ACTION_GENERATE_KEY "-g"
#define ACTION_ENCRYPT "-e"
#define ACTION_DECRYPT "-d"

void print_usage(int argc, const char *argv[])
{
	fprintf(stderr, "Usage:\n\t%s -g <path_to_key>\n\t%s <-e|-d> <path_to_input_file> <path_to_output_file>", argv[0], argv[0]);
}

int main(int argc, const char *argv[])
{
	uint8_t in_block[BLOCK_SIZE] = { 0 };
	uint8_t out_block[BLOCK_SIZE] = { 0 };
	uint8_t key[KEY_SIZE] = { 0 };
	FILE* key_file = NULL;
	FILE* in_file = NULL;
	FILE* out_file = NULL;

	if (argc < 2)
	{
		print_usage(argc, argv);
		return 1;
	}
	if (strcmp(argv[1], ACTION_GENERATE_KEY) == 0)
	{
		if (argc != 3) {
			print_usage(argc, argv);
			return 1;
		}

		key_file = fopen(argv[2], "wb");
		if (!key_file) {
			print_usage(argc, argv);
			return 1;
		}
		
		stb_genkey(key);
		
		size_t bytes_written = fwrite(key, 1, sizeof key, key_file);
		if (bytes_written != KEY_SIZE)
		{
			print_usage(argc, argv);
			fclose(key_file);
			return 1;
		}
		
		fclose(key_file);
	}
	else if ((strcmp(argv[1], ACTION_ENCRYPT) == 0) || (strcmp(argv[1], ACTION_DECRYPT) == 0)) {
		if (argc != 5) {
			print_usage(argc, argv);
			return 1;
		}

		// Read key file
		key_file = fopen(argv[2], "rb");
		if (key_file == NULL) {
			print_usage(argc, argv);
			return 1;
		}

		size_t bytes_read = fread(key, 1, sizeof key, key_file);
		if (bytes_read != KEY_SIZE)
		{
			print_usage(argc, argv);
			fclose(key_file);
			return 1;
		}
		fclose(key_file);
		
		in_file = fopen(argv[3], "rb");
		if (in_file == NULL)
		{
			print_usage(argc, argv);
			return 1;
		}

		out_file = fopen(argv[4], "wb");
		if (out_file == NULL)
		{
			print_usage(argc, argv);
			return 1;
		}
		
		uint32_t mode = 0;
		if (strcmp(argv[1], ACTION_ENCRYPT) == 0)
		{
			mode = ENCRYPTION_MODE;
			printf("Encrypting..\n");
		}
		else
		{
			mode = DECRYPTION_MODE;
			printf("Decrypting..\n");
		}
		
		clock_t start = clock();
		
		bytes_read = fread(in_block, 1, sizeof in_block, in_file);
		while (bytes_read > 0)
		{
			memset(in_block + bytes_read, 0, (sizeof in_block) - bytes_read);
			if (mode == ENCRYPTION_MODE)
			{
				stb_encrypt_block(out_block, in_block, key);
			}
			else
			{
				stb_decrypt_block(out_block, in_block, key);
			}
			fwrite(out_block, 1, sizeof out_block, out_file);
			bytes_read = fread(in_block, 1, sizeof in_block, in_file);
		}
		
		clock_t finish = clock();
		double time_taken = (double)(finish - start)/(double)CLOCKS_PER_SEC;
		printf("Finished processing %s. Time taken: %lf seconds.\n", argv[3], time_taken);
	}
	else
	{
		print_usage(argc, argv);
		return 1;
	}

    return 0;
}
