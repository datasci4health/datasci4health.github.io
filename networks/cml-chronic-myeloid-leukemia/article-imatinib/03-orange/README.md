# Orange Script

Creating your own domain with metas:

~~~python
domain = Domain([], [ContinuousVariable("logFC")],
                metas=[StringVariable("Gene.ID"),
                       StringVariable("Gene.symbol")])
~~~
