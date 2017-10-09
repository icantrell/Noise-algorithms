precision mediump float;
uniform vec2 u_resolution;
varying vec4 vColor;
unsigned int dim;
dim = 2;




float interpolate(float x0, float x1, float w){
    return (1-w)*x0 + w*x1;
}

float[dim] fade(float[dim] arr){
    float[dim] result;
    for(int i =0; i < dim; i++){
        float t;
        t = arr[i];
        result[i] =  6*t*t*t*t*t - 15*t*t*t*t + 10*t*t*t;
    }
    return result;
}


float[dim] random_grad(float[dim] pos){
    //create random gradient
    float x;
    x = 1;
    float[dim] grad;

    for(int i = 0; i < dim; i++){

        if(pos[i] != 0){
            x = x*floor(pos[i]) * 92639.0 % 40429.0;
        }
        else{
            x = x * 92639.0 % 40429.0;
        }
    }
    for(int i = 0; i < dim; i++){
        x = x*92639.0 % 40429.0;
        grad[i] = x / 40429.0;
        sum += grad[i];
    }
    for(int i = 0; i < dim; i++){
        grad[i] = grad[i] / sum;
    }

    return grad
}

float dot(float[dim] arr0,float[dim] arr1){
    //get dot product
    float sum;
    sum = 0;
    for(int i=0;i < dim; i++){
        sum += arr0[i] * arr1[i];
    }
    return sum;
}

float[dim] subtract(float[dim] arr0,float[dim] arr1){
    float[dim] arr2;
    for(int i=0;i < dim; i++){
        arr2[i] = arr0[i] * arr1[i];
    }
    return arr2;
}

float perlin(float[dim] point){
    unsigned int N;
    N = pow(2,dim);
    float[N][dim] corners;
    float[N] dot_products;

    for(int i=0; i < N; i++){
        float[dim] vec;

        for(int x=0; x < dim; x++){

            corners[i][x] = floor(point[x]);

            if(i&pow(2,x)){
                corners[i][x]++;
            }

            vec[x] = point[x] - corners[i][x];
        }

        dot_products[i] = dot(random_gradient(corner[i]), vec);

    }

    float[dim] interpolate_vec;
    interpolate_vec = fade(subtract(point,corners[0]));

    for(int d = dim; d > 0; --d){
        N = pow(2,d-1);

        for(int i = 0; i < N; ++i){
            dot_products[i] = interpolate(dot_products[i], dot_products[i+N], interpolate_vec[d-1]);
        }
    }

    return dot_products[0];
}

void main() {
    vec2 st = gl_FragCoord.xy;
    float[dim] point;
    point[0] = st.x;
    point[1] = st.y;
    float z;
    z = perlin(point);
    gl_FragColor = vec4(z,z,z,0);
}
