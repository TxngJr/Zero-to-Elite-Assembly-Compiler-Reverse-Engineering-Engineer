extern long external_value;
extern long plus_one(long);
long use_external(void) {
    return plus_one(external_value);
}
