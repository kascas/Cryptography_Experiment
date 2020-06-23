#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "murmurhash2.c"

#define MAKESTRING(n) STRING(n)
#define STRING(n) #n

struct bloom
{
  // These fields are part of the public interface of this structure.
  // Client code may read these values if desired. Client code MUST NOT
  // modify any of these.
  int entries;
  double error;
  int bits;
  int bytes;
  int hashes;

  // Fields below are private to the implementation. These may go away or
  // change incompatibly at any moment. Client code MUST NOT access or rely
  // on these.
  double bpe;
  unsigned char *bf;
  int ready;
};

int bloom_init(int entries, double error);
int bloom_init_size(int entries, double error,
                    unsigned int cache_size);
int bloom_check(const void *buffer, int len);
int bloom_add(const void *buffer, int len);
void bloom_print();
void bloom_free();
int bloom_reset();

struct bloom *bloom;

inline static int test_bit_set_bit(unsigned char *buf,
                                   unsigned int x, int set_bit)
{
  unsigned int byte = x >> 3;
  unsigned char c = buf[byte]; // expensive memory access
  unsigned int mask = 1 << (x % 8);

  if (c & mask)
  {
    return 1;
  }
  else
  {
    if (set_bit)
    {
      buf[byte] = c | mask;
    }
    return 0;
  }
}

static int bloom_check_add(const void *buffer, int len, int add)
{
  if (bloom->ready == 0)
  {
    printf("bloom at %p not initialized!\n", (void *)bloom);
    return -1;
  }

  int hits = 0;
  register unsigned int a = murmurhash2(buffer, len, 0x9747b28c);
  register unsigned int b = murmurhash2(buffer, len, a);
  register unsigned int x;
  register unsigned int i;

  for (i = 0; i < bloom->hashes; i++)
  {
    x = (a + i * b) % bloom->bits;
    if (test_bit_set_bit(bloom->bf, x, add))
    {
      hits++;
    }
    else if (!add)
    {
      // Don't care about the presence of all the bits. Just our own.
      return 0;
    }
  }

  if (hits == bloom->hashes)
  {
    return 1; // 1 == element already in (or collision)
  }

  return 0;
}

int bloom_init_size(int entries, double error,
                    unsigned int cache_size)
{
  return bloom_init(entries, error);
}

int bloom_init(int entries, double error)
{
  bloom = (struct bloom *)malloc(sizeof(struct bloom));
  bloom->ready = 0;

  if (entries < 1000 || error == 0)
  {
    return 1;
  }

  bloom->entries = entries;
  bloom->error = error;

  double num = log(bloom->error);
  double denom = 0.480453013918201; // ln(2)^2
  bloom->bpe = -(num / denom);

  double dentries = (double)entries;
  bloom->bits = (int)(dentries * bloom->bpe);

  if (bloom->bits % 8)
  {
    bloom->bytes = (bloom->bits / 8) + 1;
  }
  else
  {
    bloom->bytes = bloom->bits / 8;
  }

  bloom->hashes = (int)ceil(0.693147180559945 * bloom->bpe); // ln(2)

  bloom->bf = (unsigned char *)calloc(bloom->bytes, sizeof(unsigned char));
  if (bloom->bf == NULL)
  { // LCOV_EXCL_START
    return 1;
  } // LCOV_EXCL_STOP

  bloom->ready = 1;
  return 0;
}

int bloom_check(const void *buffer, int len)
{
  return bloom_check_add(buffer, len, 0);
}

int bloom_add(const void *buffer, int len)
{
  return bloom_check_add(buffer, len, 1);
}

void bloom_print()
{
  printf("bloom at %p\n", (void *)bloom);
  printf(" ->entries = %d\n", bloom->entries);
  printf(" ->error = %f\n", bloom->error);
  printf(" ->bits = %d\n", bloom->bits);
  printf(" ->bits per elem = %f\n", bloom->bpe);
  printf(" ->bytes = %d\n", bloom->bytes);
  printf(" ->hash functions = %d\n", bloom->hashes);
}

void bloom_free()
{
  if (bloom->ready)
  {
    free(bloom->bf);
  }
  bloom->ready = 0;
}

int bloom_reset()
{
  if (!bloom->ready)
    return 1;
  memset(bloom->bf, 0, bloom->bytes);
  return 0;
}

void bloom_write(char *filename)
{
  int i = 0;
  FILE *fp = fopen(filename, "w");
  fprintf(fp, "%d\n", bloom->entries);
  fprintf(fp, "%lf\n", bloom->error);
  fprintf(fp, "%d\n", bloom->bits);
  fprintf(fp, "%d\n", bloom->bytes);
  fprintf(fp, "%d\n", bloom->hashes);
  fprintf(fp, "%lf\n", bloom->bpe);
  for (i = 0; i < bloom->bytes; i++)
    fprintf(fp, "%d ", bloom->bf[i]);
  fprintf(fp, "\n");
  fprintf(fp, "%d\n", bloom->ready);
  fclose(fp);
  return;
}

void bloom_read(char *filename)
{
  int i = 0;
  bloom = (struct bloom *)malloc(sizeof(struct bloom));
  FILE *fp = fopen(filename, "r");
  fscanf(fp, "%d", &bloom->entries);
  fscanf(fp, "%lf", &bloom->error);
  fscanf(fp, "%d", &bloom->bits);
  fscanf(fp, "%d", &bloom->bytes);
  fscanf(fp, "%d", &bloom->hashes);
  fscanf(fp, "%lf", &bloom->bpe);
  bloom->bf = (unsigned char *)calloc(bloom->bytes, sizeof(unsigned char));
  for (i = 0; i < bloom->bytes; i++)
    fscanf(fp, "%d", &bloom->bf[i]);
  fscanf(fp, "%d", &bloom->ready);
  fclose(fp);
  return;
}
/*
int main()
{
  char str[50] = {0};
  scanf("%s", str);
  bloom_init(1000, 0.001);
  bloom_add(str, strlen(str));
  bloom_print();

  bloom_write("C:\\Users\\DELL\\Desktop\\1.json");
  bloom_reset();
  bloom_read("C:\\Users\\DELL\\Desktop\\1.json");

  printf("%d\n", bloom_check(str, strlen(str)));
  bloom_print();
  system("pause");
  return 0;
}
*/