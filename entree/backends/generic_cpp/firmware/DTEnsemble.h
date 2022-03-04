// Copyright 2022 Novel, Emerging Computing System Technologies Laboratory
//                (NECSTLab), Politecnico di Milano
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Part of this source file comes from the Conifer open-source project
// (https://github.com/thesps/conifer)

#ifndef DT_ENSEMBLE_H__
#define DT_ENSEMBLE_H__

#include <string_view>

namespace entree
{
	template <std::string_view const &node_label, int n_total_nodes, int n_trees, int n_classes, class input_t, class score_t, class threshold_t, bool direct, int n_second_level = direct ? 1 : n_classes>
	struct DTEnsemble
	{

	public:
		static constexpr const std::string_view label = node_label;

		const score_t normalisation;
		const score_t init_predict[n_classes];
		const int n_nodes_per_tree[n_trees][n_second_level];
		const int feature[n_total_nodes];
		const threshold_t threshold[n_total_nodes];
		const score_t value[n_total_nodes];
		const int children_left[n_total_nodes];
		const int children_right[n_total_nodes];
		const int parent[n_total_nodes];

		void decision_function(input_t const x, score_t score[n_classes]) const
		{
			for (int j = 0; j < n_classes; j++)
			{
				score[j] = init_predict[j];
			}

			int first_node = 0;

			for (int i = 0; i < n_trees; i++)
			{
				for (int j = 0; j < n_second_level; j++)
				{
					// TODO: Support multithreading
					score_t s = tree_decision_function(x, first_node, n_nodes_per_tree[i][j]);
					score[direct ? s : j] += 1;
					first_node += n_nodes_per_tree[i][j];
				}
			}

			if (!direct)
			{
				for (int j = 0; j < n_classes; j++)
				{
					score[j] *= normalisation;
				}
			}
		}

		score_t tree_decision_function(const input_t x, const int first_node, const int n_nodes) const
		{
			int current_node;

			for (current_node = 0; current_node < n_nodes; current_node++)
			{
				if (parent[first_node + current_node] < 0)
				{
					// Found root
					break;
				}
			}

			while (feature[first_node + current_node] >= 0)
			{
				// Tree traversing
				current_node = x[feature[first_node + current_node]] <= threshold[first_node + current_node] ? children_left[first_node + current_node] : children_right[first_node + current_node];
			}

			return value[first_node + current_node];
		}
	};
}
#endif
