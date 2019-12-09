#ifndef STB_H
#define STB_H

#include <stddef.h>
#include <stdint.h>

void stb_genkey(uint8_t *out);
void stb_encrypt_block(uint8_t *out, const uint8_t *in, const uint8_t *ks);
void stb_decrypt_block(uint8_t *out, const uint8_t *in, const uint8_t *ks);

#endif
