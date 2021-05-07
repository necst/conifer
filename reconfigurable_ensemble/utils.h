#ifndef UTILS_H__
#define UTILS_H__

#include <stddef.h>

constexpr size_t bitsizeof(unsigned int n) {
	return ((n < 2) ? 1 : 1 + bitsizeof(n / 2));
}

#endif
