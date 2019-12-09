#ifndef STB_H
#define STB_H

#include <stddef.h>
#include <stdint.h>

void stb_encrypt16(uint8_t *out, const uint8_t *in, const uint8_t *ks);
void stb_decrypt16(uint8_t *out, const uint8_t *in, const uint8_t *ks);

#endif
