/***************************/
/* FourierTransformation.c */
/***************************/

// 要素数Nの数列 a[m] をフーリエ変換で b[n] にする。添字は 0,...,N-1
// b[n] = sum[m=0,N-1]  a[m]*exp(-2*PI*I* (m/N) *n)

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <complex.h> // complex.h は fftw3.h より先に include する
#include "fftw3.h"   // windows環境では #include "C:/path/to/fftw3.h"
                     // あるいは        #include "./相対パス/fftw3.h"

int main(int argc, char *argv[])
{

    int i = 0;

    //FFTのポイント数
    int N = atoi(argv[1]);
    //サンプリング周波数
    float fs = atoi(argv[2]);

    // a,b は double _Complex 型のC99標準複素配列と実質的に同じ
    // double _Complex a[4] としても動くけど計算速度が低下する可能性あり
    fftw_complex *a, *b;
    a = (fftw_complex *)fftw_malloc(sizeof(fftw_complex) * N);
    b = (fftw_complex *)fftw_malloc(sizeof(fftw_complex) * N);

    // プランの生成
    // フーリエ逆変換つまり位相因子を exp(-k)ではなく exp(+k)とする場合は
    // FFTW_FORWARD の代わりに FFTW_BACKWARD とする
    fftw_plan plan;
    plan = fftw_plan_dft_1d(N, a, b, FFTW_FORWARD, FFTW_ESTIMATE);

    // データ読み込み
    FILE *fp; // FILE型構造体
    //char fname[] = "sample_sin.csv";
    char *fname = argv[3];
    //char fname[] = "sin.csv";
    char str[N];

    fp = fopen(fname, "r"); // ファイルを開く。失敗するとNULLを返す。
    if (fp == NULL)
    {
        printf("%s file not open!\n", fname);
        return -1;
    }
    else
    {
        printf("%s file opened!\n", fname);
    }

    while (fgets(str, N, fp) != NULL)
    {
        //printf("%.12lf\n", strtod(str, NULL));
        // フーリエ変換前の数列値を設定
        a[i] = strtod(str, NULL) + 0.0 * I;
        //printf("%lf , %lf\n", creal(a[i]), cimag(a[i]));
        i++;
    }

    fclose(fp); // ファイルを閉じる

    // フーリエ変換実行   b[n]に計算結果が入る
    fftw_execute(plan);

    fp = fopen("output.csv", "w");
    // b[n]の値を表示
    int n;
    fprintf(fp, "f[Hz],Apm.,Phase[deg]\n");
    for (n = 1; n < N/2; n++)
    {
        //printf("%+lf,%+lf\n", creal(b[n]), cimag(b[n]));
        //fprintf(fp, "%+lf,%+lf,%+lf,%+lf\n", creal(b[n]) / N * 2, cimag(b[n]) / N * 2, sqrt(pow(creal(b[n]) / N * 2, 2) + pow(cimag(b[n]) / N * 2, 2)), atan2(creal(b[n]), cimag(b[n])));
        fprintf(fp, "%+lf,%+lf,%+lf\n", (float)fs/N*n, sqrt(pow(creal(b[n]) / N * 2, 2) + pow(cimag(b[n]) / N * 2, 2)), atan2(cimag(b[n]) / N * 2, creal(b[n]) / N * 2)*180.0/M_PI);

    }
    fclose(fp);

    // ここで a[m] の値を変えて再度 fftw_execute(plan) を実行すれば、
    // b[n] が再計算される。
    printf("Done!\n");

    // 計算終了時、メモリ開放を忘れないように
    if (plan)
    fftw_destroy_plan(plan);
    fftw_free(a);
    fftw_free(b);

    return 0;
}