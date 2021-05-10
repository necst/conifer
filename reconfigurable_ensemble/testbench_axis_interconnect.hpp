#ifndef TESTBENCH_AXIS_INTERCONNECT_HPP__
#define TESTBENCH_AXIS_INTERCONNECT_HPP__

#include "hls_stream.h"

template<typename packet_t, int in_count, int out_count>
void axis_crossbar(
	hls::stream<packet_t> in[in_count],
	hls::stream<packet_t> out[out_count]
) {
	for (unsigned int i = 0; i < in_count; i++) {
		while (!in[i].empty()) {
			packet_t pkt;
			in[i] >> pkt;

			if (in_count > 1) {
				// N:1?
				unsigned int dest = 0;

				if (out_count > 1) {
					// N:M
					dest = pkt.dest;
				}

				if (dest > out_count) {
					std::cout << "Unable to route axis packet from stream " << i << " to stream " << dest << std::endl;
					continue;
				}

				out[dest] << pkt;
			} else {
				// 1:N
				for (unsigned int j = 0; j < out_count; j++) {
					out[j] << pkt;
				}
			}
		}
	}
}

#endif
