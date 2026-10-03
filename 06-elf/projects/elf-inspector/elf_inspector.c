#include <elf.h>
#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { unsigned char *data; size_t size; } FileImage;

static int range_ok(size_t off, size_t count, size_t elem, size_t total) {
    if (elem != 0 && count > (SIZE_MAX - off) / elem) return 0;
    return off <= total && count * elem <= total - off;
}
static int load_file(const char *path, FileImage *img) {
    FILE *f = fopen(path, "rb");
    if (!f) { fprintf(stderr, "%s: %s\n", path, strerror(errno)); return 0; }
    if (fseek(f, 0, SEEK_END) != 0) { fclose(f); return 0; }
    long n = ftell(f);
    if (n < 0 || fseek(f, 0, SEEK_SET) != 0) { fclose(f); return 0; }
    img->size = (size_t)n;
    img->data = img->size ? malloc(img->size) : NULL;
    if (img->size && !img->data) { fclose(f); return 0; }
    if (img->size && fread(img->data, 1, img->size, f) != img->size) {
        free(img->data); img->data = NULL; fclose(f); return 0;
    }
    fclose(f); return 1;
}
static const char *etype(uint16_t t) {
    switch (t) {
        case ET_REL: return "REL"; case ET_EXEC: return "EXEC";
        case ET_DYN: return "DYN"; case ET_CORE: return "CORE";
        default: return "OTHER";
    }
}
static const char *ph_type(uint32_t t) {
    switch (t) {
        case PT_NULL: return "NULL"; case PT_LOAD: return "LOAD";
        case PT_DYNAMIC: return "DYNAMIC"; case PT_INTERP: return "INTERP";
        case PT_NOTE: return "NOTE"; case PT_PHDR: return "PHDR";
        default: return "OTHER";
    }
}
static int valid_string(const char *base, size_t size, size_t off) {
    if (off >= size) return 0;
    return memchr(base + off, '\0', size - off) != NULL;
}
int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: %s FILE\n", argv[0]); return 2; }
    FileImage img = {0};
    if (!load_file(argv[1], &img)) return 1;
    if (img.size < sizeof(Elf64_Ehdr)) {
        fputs("not a complete ELF64 header\n", stderr); free(img.data); return 1;
    }
    Elf64_Ehdr eh;
    memcpy(&eh, img.data, sizeof eh);
    if (memcmp(eh.e_ident, ELFMAG, SELFMAG) != 0 ||
        eh.e_ident[EI_CLASS] != ELFCLASS64 ||
        eh.e_ident[EI_DATA] != ELFDATA2LSB ||
        eh.e_ident[EI_VERSION] != EV_CURRENT) {
        fputs("unsupported or invalid ELF64 little-endian file\n", stderr);
        free(img.data); return 1;
    }
    if (eh.e_ehsize != sizeof(Elf64_Ehdr)) {
        fputs("unexpected ELF header size\n", stderr); free(img.data); return 1;
    }
    printf("ELF64 type=%s machine=%u entry=0x%" PRIx64 "\n",
           etype(eh.e_type), (unsigned)eh.e_machine, (uint64_t)eh.e_entry);
    printf("program_headers=%u section_headers=%u\n",
           (unsigned)eh.e_phnum, (unsigned)eh.e_shnum);

    if (eh.e_phnum) {
        if (eh.e_phentsize != sizeof(Elf64_Phdr) ||
            !range_ok((size_t)eh.e_phoff, eh.e_phnum, sizeof(Elf64_Phdr), img.size)) {
            fputs("invalid program header table\n", stderr); free(img.data); return 1;
        }
        for (size_t i = 0; i < eh.e_phnum; ++i) {
            Elf64_Phdr ph;
            memcpy(&ph, img.data + (size_t)eh.e_phoff + i * sizeof ph, sizeof ph);
            printf("PH[%zu] %-7s off=0x%" PRIx64 " vaddr=0x%" PRIx64
                   " filesz=0x%" PRIx64 " memsz=0x%" PRIx64 " flags=%c%c%c\n",
                   i, ph_type(ph.p_type), (uint64_t)ph.p_offset, (uint64_t)ph.p_vaddr,
                   (uint64_t)ph.p_filesz, (uint64_t)ph.p_memsz,
                   (ph.p_flags & PF_R) ? 'R' : '-',
                   (ph.p_flags & PF_W) ? 'W' : '-',
                   (ph.p_flags & PF_X) ? 'X' : '-');
        }
    }

    if (eh.e_shnum) {
        if (eh.e_shentsize != sizeof(Elf64_Shdr) ||
            !range_ok((size_t)eh.e_shoff, eh.e_shnum, sizeof(Elf64_Shdr), img.size) ||
            eh.e_shstrndx >= eh.e_shnum) {
            fputs("invalid section header table\n", stderr); free(img.data); return 1;
        }
        Elf64_Shdr shstr;
        memcpy(&shstr, img.data + (size_t)eh.e_shoff +
               (size_t)eh.e_shstrndx * sizeof shstr, sizeof shstr);
        if (!range_ok((size_t)shstr.sh_offset, 1, (size_t)shstr.sh_size, img.size)) {
            fputs("invalid section-name string table\n", stderr); free(img.data); return 1;
        }
        const char *names = (const char *)img.data + (size_t)shstr.sh_offset;
        size_t names_size = (size_t)shstr.sh_size;
        for (size_t i = 0; i < eh.e_shnum; ++i) {
            Elf64_Shdr sh;
            memcpy(&sh, img.data + (size_t)eh.e_shoff + i * sizeof sh, sizeof sh);
            const char *name = "<bad-name>";
            if (valid_string(names, names_size, sh.sh_name)) name = names + sh.sh_name;
            printf("SH[%zu] %-18s type=%u off=0x%" PRIx64 " size=0x%" PRIx64 "\n",
                   i, name, (unsigned)sh.sh_type,
                   (uint64_t)sh.sh_offset, (uint64_t)sh.sh_size);
        }
    }
    free(img.data); return 0;
}
