# Transforms 2D

Rotação por θ:

```
| cosθ  -sinθ |   |x|
| sinθ   cosθ | · |y|
```

Translação: `p' = R·p + t`.

Homogêneo 3×3 empacota R e t numa só matriz — padrão em ROS / robótica.
