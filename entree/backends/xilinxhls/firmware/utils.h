// Copyright 2022 Novel, Emerging Computing System Technologies Laboratory 
//                (NECSTLab), Politecnico di Milano

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef UTILS_H__
#define UTILS_H__

#include <stddef.h>

constexpr size_t bitsizeof(unsigned int n) {
	return ((n < 2) ? 1 : 1 + bitsizeof(n / 2));
}

#endif
