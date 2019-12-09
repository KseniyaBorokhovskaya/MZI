#include <stdio.h>
#include <stdbool.h>
#include <string.h>

#include "stb.h"

void print_usage(int argc, const char *argv[])
{
	fprintf(stderr, "Usage: %s <path_to_key> <is_encrypt> <path_to_input_file> <path_to_output_file>", argv[0]);
}

int main(int argc, const char *argv[])
{
	uint8_t in_block[16] = { 0 };
	uint8_t out_block[16] = { 0 };
	uint8_t key[32] = { 0 };
	uint32_t is_encrypt = 0;
	FILE* in_key = NULL;
	FILE* in_file = NULL;
	FILE* out_file = NULL;

	if (argc < 5)
	{
		print_usage(argc, argv);
		return 1;
	}

	in_key = fopen(argv[1], "rb");
	if (in_key == NULL)
	{
		print_usage(argc, argv);
		return 1;
	}
	fread(key, sizeof(unsigned char), sizeof key, in_key);

	if (sscanf(argv[2], "%d", &is_encrypt) != 1)
	{
		print_usage(argc, argv);
		return 1;
	}

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

	size_t read_bytes = fread(in_block, sizeof(unsigned char), sizeof in_block, in_file);
	while (read_bytes > 0) {
		if (is_encrypt) {
			stb_encrypt16(out_block, in_block, key);
		}
		else {
			stb_decrypt16(out_block, in_block, key);
		}
		fwrite(out_block, sizeof(unsigned char), sizeof out_block, out_file);
		read_bytes = fread(in_block, sizeof(unsigned char), sizeof in_block, in_file);
	}

    return 0;
}
