#ifndef UTILS_HPP__
#define UTILS_HPP__

#include <boost/preprocessor/repetition/enum_params.hpp>
#include <boost/preprocessor/iteration/local.hpp>

#define GENERATE_PRAGMA(x) 	_Pragma(#x)
#define CALL(macro, ...)  	macro(__VA_ARGS__)

#define GEN_ARRAY_AXIS_PARAMS(type, name, count)                        \
    BOOST_PP_ENUM_PARAMS(count, type name)

#define GEN_ARRAY_AXIS_PRAGMA(type, name, n)                            \
    GENERATE_PRAGMA(                                                    \
        HLS INTERFACE axis register_mode=both register port=name ## n   \
    )

#define GEN_ARRAY_AXIS_ITEM(z, n, name)                                 \
    name[n] = name ## n;

#define GEN_ARRAY_AXIS_ARRAY(type, name, count)                          \
    type name[count];                                                    \
    BOOST_PP_REPEAT(count, GEN_ARRAY_AXIS_ITEM, name)

#endif
