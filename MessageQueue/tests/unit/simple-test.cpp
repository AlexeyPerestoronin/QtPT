#include <gtest/gtest.h>

TEST(MathFunctions, Addition) {
    EXPECT_EQ(2 + 2, 4);
}

TEST(LogicFunctions, IsTrue) {
    bool result = true;
    ASSERT_TRUE(result);
}