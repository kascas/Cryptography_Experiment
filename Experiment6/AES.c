#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "AES128.h"
#include <time.h>

void pkcs_7(uint8 *content, int len)
{
    int i = 0;
    if (len != 16 && len != 0)
    {
        int pos = len % 16;
        for (i = pos; i < 16; i++)
            content[i] = 16 - len;
    }
    else if (len == 0)
        for (i = 0; i < 16; i++)
            content[i] = 0x10;
    return;
}

int filesize(FILE *fp)
{
    unsigned int file_size = 0;
    fseek(fp, 0, SEEK_END);
    file_size = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    return file_size;
}

void bytesxor(uint8 *a, uint8 *b)
{
    int i = 0;
    for (i = 0; i < 16; i++)
        a[i] ^= b[i];
    return;
}

void AES_ECB_encrypt(char *src, char *dest, uint8 *key)
{
    uint8 buffer[16] = {0};
    FILE *fp = fopen(src, "rb");
    FILE *f_write = fopen(dest, "wb");
    int readlen = 0;
    while (1)
    {
        readlen = fread(buffer, 1, 16, fp);
        pkcs_7(buffer, readlen);
        encrypt(buffer, key);
        fwrite(buffer, 1, 16, f_write);
        if (readlen != 16 || readlen == 0)
            break;
    }
    fclose(fp);
    fclose(f_write);
    return;
}

void AES_ECB_decrypt(char *src, char *dest, uint8 *key)
{
    uint8 buffer[16] = {0};
    FILE *fp = fopen(src, "rb");
    FILE *f_write = fopen(dest, "wb");
    int total = filesize(fp) / 16;
    int readlen = 0, count = 0;
    while (1)
    {
        count++;
        readlen = fread(buffer, 1, 16, fp);
        if (readlen == 0)
            break;
        decrypt(buffer, key);
        int write_len = 16;
        if (count == total)
            write_len = 16 - buffer[15];
        fwrite(buffer, 1, write_len, f_write);
    }
    fclose(fp);
    fclose(f_write);
    return;
}

void AES_CBC_encrypt(char *src, char *dest, uint8 *key, uint8 *IV)
{
    uint8 buffer[16] = {0};
    uint8 *xor_in = IV;
    FILE *fp = fopen(src, "rb");
    FILE *f_write = fopen(dest, "wb");
    int readlen = 0;
    int i = 0;
    while (1)
    {
        readlen = fread(buffer, 1, 16, fp);
        pkcs_7(buffer, readlen);
        bytesxor(buffer, xor_in);
        encrypt(buffer, key);
        for (i = 0; i < 16; i++)
            xor_in[i] = buffer[i];
        fwrite(buffer, 1, 16, f_write);
        if (readlen != 16 || readlen == 0)
            break;
    }
    fclose(fp);
    fclose(f_write);
    return;
}

void AES_CBC_decrypt(char *src, char *dest, uint8 *key, uint8 *IV)
{
    uint8 buffer[16] = {0}, tmp[16] = {0};
    uint8 *xor_in = IV;
    FILE *fp = fopen(src, "rb");
    FILE *f_write = fopen(dest, "wb");
    int total = filesize(fp) / 16;
    int readlen = 0, count = 0;
    int i = 0;
    while (1)
    {
        count++;
        readlen = fread(buffer, 1, 16, fp);
        if (readlen == 0)
            break;
        for (i = 0; i < 16; i++)
            tmp[i] = buffer[i];
        decrypt(buffer, key);
        bytesxor(buffer, xor_in);
        for (i = 0; i < 16; i++)
            xor_in[i] = tmp[i];
        int write_len = 16;
        if (count == total)
            write_len = 16 - buffer[15];
        fwrite(buffer, 1, write_len, f_write);
    }
    fclose(fp);
    fclose(f_write);
    return;
}

void AES_OFB_encrypt(char *src, char *dest, uint8 *key, uint8 *IV)
{
    uint8 buffer[1] = {0}, select = 0;
    uint8 *reg = IV, x[16] = {0};
    FILE *fp = fopen(src, "rb");
    FILE *f_write = fopen(dest, "wb");
    int readlen = 0;
    int i = 0;
    while (1)
    {
        readlen = fread(buffer, 1, 1, fp);
        if (readlen == 0)
            break;
        for (i = 0; i < 16; i++)
            x[i] = reg[i];
        encrypt(x, key);
        buffer[0] ^= x[0];
        fwrite(buffer, 1, 1, f_write);
        for (i = 0; i < 16; i++)
            reg[i] = reg[i + 1];
        reg[15] = x[0];
    }
    fclose(fp);
    fclose(f_write);
    return;
}

void AES_OFB_decrypt(char *src, char *dest, uint8 *key, uint8 *IV)
{
    uint8 buffer[1] = {0}, select = 0;
    uint8 *reg = IV, x[16] = {0};
    FILE *fp = fopen(src, "rb");
    FILE *f_write = fopen(dest, "wb");
    int readlen = 0;
    int i = 0;
    while (1)
    {
        readlen = fread(buffer, 1, 1, fp);
        if (readlen == 0)
            break;
        for (i = 0; i < 16; i++)
            x[i] = reg[i];
        encrypt(x, key);
        buffer[0] ^= x[0];
        fwrite(buffer, 1, 1, f_write);
        for (i = 0; i < 16; i++)
            reg[i] = reg[i + 1];
        reg[15] = x[0];
    }
    fclose(fp);
    fclose(f_write);
    return;
}

void AES_CFB_encrypt(char *src, char *dest, uint8 *key, uint8 *IV)
{
    uint8 buffer[1] = {0}, select = 0;
    uint8 *reg = IV, x[16] = {0};
    FILE *fp = fopen(src, "rb");
    FILE *f_write = fopen(dest, "wb");
    int readlen = 0;
    int i = 0;
    while (1)
    {
        readlen = fread(buffer, 1, 1, fp);
        if (readlen == 0)
            break;
        for (i = 0; i < 16; i++)
            x[i] = reg[i];
        encrypt(x, key);
        buffer[0] ^= x[0];
        fwrite(buffer, 1, 1, f_write);
        for (i = 0; i < 16; i++)
            reg[i] = reg[i + 1];
        reg[15] = buffer[0];
    }
    fclose(fp);
    fclose(f_write);
    return;
}

void AES_CFB_decrypt(char *src, char *dest, uint8 *key, uint8 *IV)
{
    uint8 buffer[1] = {0}, select = 0;
    uint8 *reg = IV, x[16] = {0};
    FILE *fp = fopen(src, "rb");
    FILE *f_write = fopen(dest, "wb");
    int readlen = 0;
    int i = 0;
    while (1)
    {
        readlen = fread(buffer, 1, 1, fp);
        if (readlen == 0)
            break;
        for (i = 0; i < 16; i++)
            x[i] = reg[i];
        encrypt(x, key);
        buffer[0] ^= x[0];
        fwrite(buffer, 1, 1, f_write);
        for (i = 0; i < 16; i++)
            reg[i] = reg[i + 1];
        reg[15] = buffer[0];
    }
    fclose(fp);
    fclose(f_write);
    return;
}
/*
int main()
{
    char src[30] = "F:/GitWS/Code/in.png";
    char dest[30] = "F:/GitWS/Code/out.png";
    uint8 key[16] = {0x0f, 0x15, 0x71, 0xc9, 0x47, 0xd9, 0xe8, 0x59, 0x0c, 0xb7, 0xad, 0xd6, 0xaf, 0x7f, 0x67, 0x98};
    uint8 IV1[16] = {0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1};
    uint8 IV2[16] = {0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1};
    AES_OFB_encrypt(src, dest, key, IV1);
    int start = clock();
    AES_OFB_decrypt("F:/GitWS/Code/out.png", "F:/GitWS/Code/new.png", key, IV2);
    int end = clock();
    printf("time: %llf", ((double)(end - start) / CLOCKS_PER_SEC));
    system("pause");
    return 0;
}
*/