#include "voting_station.hpp"

#define SAMPLES 3
#define BATCHES 3

int check_output(hls::stream<output_s_t> &output_class_stream, double in_gold) {
	if (output_class_stream.empty()) {
		std::cerr << "Output Stream is empty but should contain a result!" << std::endl;
		return -10;
	}

	output_s_t out;
	output_class_stream >> out;
	if (fabs(out.data.to_double() - (double)in_gold) > 0.000000000000000001) {
		std::cerr << "Output is " << out.data << " and should be " << in_gold << std::endl;
		return -11;
	}

	std::cerr << "Output is " << out.data << " (gold value: " << in_gold << ")" << std::endl;
	return 0;
}

int main(int argc, char* argv[]) {
	score_t values[BATCHES][SAMPLES] = { { 2.5, 3.5, 4.5 }, { 2.0, 3.0, 4.0 }, { 1.5, 2.5, 3.5 } };
	score_t in_gold;

	hls::stream<input_s_t> input_class_stream;
	hls::stream<output_s_t> output_class_stream;

	for(unsigned int id = 0; id < BATCHES; id++) {
		for(unsigned int i = 0; i < SAMPLES; i++) {
			input_s_t in;

			in.data = values[id][i];
			in.id   = id;
			in.last = false;

			input_class_stream << in;

			voting_station(input_class_stream, output_class_stream);

			if (i == 0) {
				if (id > 0) {
					int ret = check_output(output_class_stream, in_gold);
					if (ret != 0) {
						return ret;
					}
				}

				in_gold = init_predict;
			} else {
				if (!output_class_stream.empty()) {
					std::cerr << "Output Stream should be empty but is not!" << std::endl;
					return -1;
				}
			}

			in_gold += values[id][i];
		}
	}

	input_s_t in;

	in.data = 0.0;
	in.id   = 0;
	in.last = true;

	input_class_stream << in;

	voting_station(input_class_stream, output_class_stream);

	check_output(output_class_stream, in_gold);

	return 0;
}
