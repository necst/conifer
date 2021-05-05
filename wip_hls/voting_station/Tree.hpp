#ifndef TREE_HPP__
#define TREE_HPP__

constexpr size_t bitsizeof(unsigned int n) {
	return ((n < 2) ? 1 : 1 + bitsizeof(n / 2));
}

#endif
